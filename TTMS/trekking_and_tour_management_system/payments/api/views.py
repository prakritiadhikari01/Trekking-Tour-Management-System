import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bookings.models import Booking
from payments.models import Payment
from django.http import HttpResponse


# =========================
# INITIATE PAYMENT
# =========================
class KhaltiInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            booking_id = request.data.get("booking_id")

            booking = Booking.objects.get(id=booking_id, user=request.user)

            # create or get payment
            payment, created = Payment.objects.get_or_create(
                booking=booking,
                user=request.user,
                defaults={
                    "amount": booking.total_price,
                    "status": "PENDING"
                }
            )

            # IMPORTANT: DO NOT use verify URL here
            payload = {
                "return_url": "http://127.0.0.1:8000/api/payments/payment/success/",
                "website_url": "http://127.0.0.1:8000",
                "amount": int(payment.amount * 100),  # paisa
                "purchase_order_id": str(payment.id),
                "purchase_order_name": f"Booking #{booking.id}",
            }

            headers = {
                "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                settings.KHALTI_INITIATE_URL,
                json=payload,
                headers=headers
            )

            data = response.json()

            if response.status_code == 200:
                payment.pidx = data.get("pidx")
                payment.save()

                return Response({
                    "message": "Payment initiated",
                    "payment_url": data.get("payment_url"),
                    "pidx": payment.pidx
                })

            return Response(data, status=400)

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


# =========================
# VERIFY PAYMENT
# =========================
class KhaltiVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pidx = request.data.get("pidx")

            if not pidx:
                return Response({"error": "pidx is required"}, status=400)

            # IMPORTANT: user check added
            payment = Payment.objects.get(
                pidx=pidx,
                user=request.user
            )

            headers = {
                "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                settings.KHALTI_LOOKUP_URL,
                json={"pidx": pidx},
                headers=headers
            )

            data = response.json()

            # =========================
            # PAYMENT SUCCESS
            # =========================
            if data.get("status") == "Completed":

                payment.status = "PAID"
                payment.transaction_id = (
                    data.get("transaction_id")
                    or data.get("idx")
                    or pidx
                )
                payment.save()

                booking = payment.booking

                # adjust field name if needed
                booking.status = "CONFIRMED"
                booking.save()

                return Response({
                    "message": "Payment successful",
                    "booking_id": booking.id,
                    "transaction_id": payment.transaction_id
                })

            # =========================
            # PAYMENT FAILED / PENDING
            # =========================
            payment.status = "FAILED"
            payment.save()

            return Response({
                "message": "Payment not completed",
                "data": data
            }, status=400)

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
def payment_success(request):
    return HttpResponse("Payment Successful You can close this page.")        
