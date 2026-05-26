# from django.shortcuts import get_object_or_404, redirect
# from django.conf import settings
# from django.http import HttpResponse
# from decimal import Decimal
# import requests

# from bookings.models import Booking
# from .models import Payment


# def khalti_payment(request, booking_id):

#     booking = get_object_or_404(Booking, id=booking_id)

#     payment, created = Payment.objects.get_or_create(
#         booking=booking,
#         user=booking.user,
#         defaults={
#             "amount": booking.total_price,
#             "status": "PENDING"
#         }
#     )

#     amount_in_paisa = int(Decimal(booking.total_price) * 100)

#     if amount_in_paisa < 1000:
#         return HttpResponse("Minimum payment is Rs.10")

#     payload = {
#         "return_url": request.build_absolute_uri("/payments/success/"),
#         "website_url": request.build_absolute_uri("/"),
#         "amount": amount_in_paisa,
#         "purchase_order_id": str(booking.id),
#         "purchase_order_name": booking.package.title,
#         "customer_info": {
#             "name": booking.full_name,
#             "email": booking.email,
#             "phone": booking.phone_number,
#         },
#     }

#     headers = {
#         "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(
#         settings.KHALTI_INITIATE_URL,
#         json=payload,
#         headers=headers
#     )

#     data = response.json()

#     if response.status_code == 200 and "payment_url" in data:
#         payment.khalti_pidx = data.get("pidx")
#         payment.save()
#         return redirect(data["payment_url"])

#     return HttpResponse(f"Payment Failed: {data}")


# def payment_success(request):

#     pidx = request.GET.get("pidx")
#     booking_id = request.GET.get("purchase_order_id")

#     headers = {
#         "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
#         "Content-Type": "application/json",
#     }

#     response = requests.post(
#         settings.KHALTI_LOOKUP_URL,
#         json={"pidx": pidx},
#         headers=headers
#     )

#     data = response.json()

#     if data.get("status") == "Completed":

#         booking = Booking.objects.filter(id=booking_id).first()

#         if booking:
#             booking.booking_status = "CONFIRMED"
#             booking.save()

#             payment = Payment.objects.filter(booking=booking).first()

#             if payment:
#                 payment.status = "COMPLETED"
#                 payment.transaction_id = pidx
#                 payment.save()

#             return redirect("bookings:booking_success")

#     return redirect("payments:payment_failed")

# from django.http import HttpResponse

# def payment_success(request):
#     return HttpResponse("Payment Successful. You can close this page.")