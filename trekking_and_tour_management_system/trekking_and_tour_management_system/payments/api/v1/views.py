import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.payments.models import Invoice, Payment
from trekking_and_tour_management_system.payments.services.invoice_service import generate_or_update_invoice
from trekking_and_tour_management_system.payments.services.khalti_service import ensure_khalti_payment_link

class KhaltiInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            booking_id = request.data.get("booking_id")

            if not booking_id:
                return Response({"error": "booking_id is required"}, status=400)

            booking = Booking.objects.get(id=booking_id, user=request.user)

            # prevent multiple pending payments
            payment = Payment.objects.filter(
                booking=booking,
                status="PENDING"
            ).first()

            if not payment:
                payment = Payment.objects.create(
                    booking=booking,
                    user=request.user,
                    amount=booking.total_price,
                    status="PENDING"
                )
            try:
                payment = ensure_khalti_payment_link(payment)
            except requests.RequestException as e:
                return Response({"error": "Khalti request failed", "details": str(e)}, status=500)
            except ValueError as e:
                return Response({"error": str(e)}, status=500)

            return Response({
                "message": "Payment initiated",
                "payment_url": payment.payment_url,
                "pidx": payment.pidx
            })

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class KhaltiVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pidx = request.data.get("pidx")

            if not pidx:
                return Response({"error": "pidx is required"}, status=400)

            payment = Payment.objects.select_related("booking").get(
                pidx=pidx,
                user=request.user
            )

            try:
                response = requests.post(
                    settings.KHALTI_LOOKUP_URL,
                    json={"pidx": pidx},
                    headers={
                        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=10
                )
            except requests.RequestException as e:
                return Response({"error": "Khalti verify failed", "details": str(e)}, status=500)

            if response.status_code != 200:
                return Response({
                    "error": "Khalti verification failed",
                    "details": response.text
                }, status=400)

            data = response.json()

            
            if data.get("status") == "Completed":

                with transaction.atomic():
                    payment.status = "COMPLETED"
                    payment.transaction_id = (
                        data.get("transaction_id")
                        or data.get("idx")
                        or pidx
                    )
                    payment.save(update_fields=["status", "transaction_id"])
                    booking = payment.booking
                    booking.booking_status = "CONFIRMED"
                    booking.save(update_fields=["booking_status", "updated_at"])

                return Response({
                    "message": "Payment successful",
                    "payment_status": payment.status,
                    "booking_status": booking.booking_status,
                    "booking_id": booking.id,
                    "transaction_id": payment.transaction_id
                })

            booking = payment.booking
            payment.status = "FAILED"
            payment.save(update_fields=["status"])

            return Response({
                "message": "Payment not completed",
                "payment_status": payment.status,
                "booking_status": booking.booking_status,
                "status": data.get("status"),
                "data": data
            }, status=400)

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

#API view to return invoice data as JSON
class InvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pidx = request.query_params.get("pidx")

        if not pidx:
            return Response({"error": "pidx is required"}, status=400)

        try:
            payment = Payment.objects.select_related(
                "booking",
                "booking__package",
                "user"
            ).get(
                pidx=pidx,
                user=request.user
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        booking = payment.booking
        package = booking.package

        # ❗ ensure payment is completed
        if payment.status != "COMPLETED":
            return Response(
                {"error": "Invoice not available. Payment not completed."},
                status=400
            )

        invoice = getattr(payment, "invoice", None)
        if invoice is None:
            return Response({"error": "Invoice is being generated. Please retry shortly."}, status=202)

        base_url = getattr(settings, "APP_BASE_URL", "").rstrip("/")
        invoice_data = {
            "invoice_id": invoice.invoice_id,
            "customer_name": booking.full_name,
            "email": booking.email,
            "phone_number": booking.phone_number,

            "package_title": package.title,
            "package_price": str(package.price),

            "trip_start_date": booking.trip_start_date,
            "trip_end_date": booking.trip_end_date,
            "number_of_people": booking.number_of_people,

            "total_amount": str(payment.amount),

            "payment_status": payment.status,
            "booking_status": booking.booking_status,
            "transaction_id": payment.transaction_id,
            "khalti_pidx": payment.pidx,
            "created_at": payment.created_at,
            "invoice_url": f"{base_url}/api/payments/invoices/{invoice.access_token}/download/",
        }

        return Response(invoice_data)

class DownloadInvoiceByTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        try:
            invoice = Invoice.objects.select_related("payment", "booking").get(
                access_token=token,
            )
        except Invoice.DoesNotExist:
            return HttpResponse("Invoice not found", status=404)

        if invoice.booking.user_id != request.user.id and not request.user.is_staff:
            return HttpResponse("Not authorized", status=403)
        if not invoice.file:
            return HttpResponse("Invoice file is not ready", status=404)
        return HttpResponse(
            invoice.file.read(),
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{invoice.invoice_id}.pdf"',
            },
        )


class DownloadInvoiceByPidxView(APIView):
    """
    Backward-compatible invoice endpoint:
    /api/payments/download-invoice/<pidx>/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pidx):
        try:
            payment = Payment.objects.select_related("booking").get(
                pidx=pidx,
                user=request.user,
            )
        except Payment.DoesNotExist:
            return HttpResponse("Payment not found", status=404)

        if payment.status != "COMPLETED":
            return HttpResponse("Invoice not available", status=400)

        invoice = getattr(payment, "invoice", None)
        if not invoice or not invoice.file:
            try:
                invoice = generate_or_update_invoice(payment.id)
            except ValueError:
                return HttpResponse("Invoice not available", status=400)

        return HttpResponse(
            invoice.file.read(),
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{invoice.invoice_id}.pdf"',
            },
        )