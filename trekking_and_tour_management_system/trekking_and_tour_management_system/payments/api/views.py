from urllib import response

import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.payments.models import Payment

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

            payload = {
                "return_url": "http://127.0.0.1:8000/api/payments/verify/",
                "website_url": "http://127.0.0.1:8000",
                "amount": int(payment.amount * 100),
                "purchase_order_id": str(payment.id),
                "purchase_order_name": f"Booking #{booking.id}",
            }

            try:
                response = requests.post(
                    settings.KHALTI_INITIATE_URL,
                    json=payload,
                    headers={
                        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=10
                )
            except requests.RequestException as e:
                return Response({"error": "Khalti request failed", "details": str(e)}, status=500)

            if response.status_code != 200:
                return Response({
                    "error": "Khalti initiate failed",
                    "details": response.text
                }, status=400)

            data = response.json()

            if not data.get("pidx") or not data.get("payment_url"):
                return Response({"error": "Invalid Khalti response"}, status=500)

            payment.pidx = data["pidx"]
            payment.save()

            return Response({
                "message": "Payment initiated",
                "payment_url": data["payment_url"],
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
                    payment.save()

                    booking = payment.booking
                    booking.payment_status = "COMPLETED" 
                    booking.booking_status = "CONFIRMED"  # adjust if needed
                    booking.save()

                    # generate_invoice_pdf(payment)

                return Response({
                    "message": "Payment successful",
                    "payment_status": payment.status,
                    "booking_status": booking.booking_status,
                    "booking_id": booking.id,
                    "transaction_id": payment.transaction_id
                })

           
            payment.status = "FAILED"
            payment.save()

            return Response({
                "message": "Payment not completed",
                "payment_status": payment.status,
                "booking_status": booking.payment_status,
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

        invoice_data = {
            "invoice_id": f"INV-{payment.id}",
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
        }

        return Response(invoice_data)

        
class DownloadInvoicePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pidx):

        try:
            payment = Payment.objects.select_related(
                "booking",
                "booking__package"
            ).get(
                pidx=pidx,
                user=request.user
            )

        except Payment.DoesNotExist:
            return HttpResponse("Payment not found", status=404)

        if payment.status != "COMPLETED":
            return HttpResponse("Invoice not available", status=400)

        booking = payment.booking
        package = booking.package

        # =====================================
        # CREATE PDF
        # =====================================
        buffer = BytesIO()

        p = canvas.Canvas(buffer, pagesize=A4)

        width, height = A4

        # =====================================
        # TOP HEADER BAR
        # =====================================
        p.setFillColor(colors.HexColor("#0F172A"))
        p.rect(0, height - 90, width, 90, fill=True, stroke=False)

        # COMPANY TITLE
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 24)
        p.drawString(50, height - 50, "TREKKING & TOUR")

        p.setFont("Helvetica", 12)
        p.drawString(50, height - 72, "Professional Travel Invoice")

        # =====================================
        # INVOICE TITLE
        # =====================================
        p.setFillColor(colors.HexColor("#111827"))
        p.setFont("Helvetica-Bold", 20)
        p.drawString(400, height - 130, "INVOICE")

        p.setFont("Helvetica", 11)
        p.drawString(400, height - 150, f"Invoice ID: INV-{payment.id}")
        p.drawString(400, height - 168, f"Date: {payment.created_at.date()}")

        # =====================================
        # COMPANY INFO
        # =====================================
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 140, "Company Details")

        p.setFont("Helvetica", 10)
        p.drawString(50, height - 160, "Trekking & Tour Management System")
        p.drawString(50, height - 176, "Pokhara, Nepal")
        p.drawString(50, height - 192, "support@trekking.com")
        p.drawString(50, height - 208, "+977-98XXXXXXXX")

        # =====================================
        # CUSTOMER INFO BOX
        # =====================================
        p.setFillColor(colors.HexColor("#F3F4F6"))
        p.roundRect(40, height - 340, 520, 90, 10, fill=True, stroke=False)

        p.setFillColor(colors.black)

        p.setFont("Helvetica-Bold", 13)
        p.drawString(55, height - 275, "Customer Details")

        p.setFont("Helvetica", 11)
        p.drawString(55, height - 295, f"Name: {booking.full_name}")
        p.drawString(55, height - 313, f"Email: {booking.email}")
        p.drawString(320, height - 295, f"Phone: {booking.phone_number}")
        p.drawString(320, height - 313, f"Trip Start Date: {booking.trip_start_date}")
        p.drawString(320, height - 331, f"Trip End Date: {booking.trip_end_date}")

        # =====================================
        # BOOKING TABLE
        # =====================================
        payment_display = (
            "Paid"
            if payment.status == "COMPLETED"
            else payment.status.title()
)
        booking_display = booking.booking_status.title()
        table_data = [
            [
                "Package",
                "People",
                "Price",
                "Payment",
                "Booking"
            ],
            [
                package.title,
                str(booking.number_of_people),
                f"NPR {payment.amount}",
                payment_display,
                booking_display
            ]
        ]

        table = Table(table_data, colWidths=[180, 70, 90, 90, 90])

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))

        table.wrapOn(p, width, height)
        table.drawOn(p, 40, height - 470)

        # =====================================
        # TOTAL BOX
        # =====================================
        p.setFillColor(colors.HexColor("#DCFCE7"))
        p.roundRect(350, height - 560, 190, 70, 10, fill=True, stroke=False)

        p.setFillColor(colors.black)

        p.setFont("Helvetica-Bold", 14)
        p.drawString(370, height - 520, "TOTAL PAID")

        p.setFont("Helvetica-Bold", 18)
        p.drawString(370, height - 545, f"NPR {payment.amount}")

        # =====================================
        # TRANSACTION INFO
        # =====================================
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 530, "Transaction Details")

        p.setFont("Helvetica", 11)
        p.drawString(50, height - 555, f"Transaction ID: {payment.transaction_id}")
        p.drawString(50, height - 575, f"Khalti PIDX: {payment.pidx}")

        # =====================================
        # FOOTER
        # =====================================
        p.setStrokeColor(colors.HexColor("#CBD5E1"))
        p.line(40, 80, 550, 80)

        p.setFont("Helvetica-Oblique", 10)
        p.drawString(170, 60, "Thank you for booking with us!")

        p.setFont("Helvetica", 9)
        p.drawString(150, 45, "Generated by Trekking & Tour Management System")

        # SAVE PDF
        p.showPage()
        p.save()

        # IMPORTANT
        buffer.seek(0)

        return HttpResponse(
            buffer.getvalue(),
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="invoice_{payment.id}.pdf"'
            }
        )