import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bookings.models import Booking
from payments.models import Payment


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
                "return_url": "http://127.0.0.1:8000/api/payments/payment/success/",
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
                    booking.payment_status = "paid" 
                    booking.booking_status = "confirmed"  # adjust if needed
                    booking.save()

                return Response({
                    "message": "Payment successful",
                    "payment_status": payment.status,
                    "booking_status": booking.payment_status,
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