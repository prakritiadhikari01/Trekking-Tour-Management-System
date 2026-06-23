from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from payments.models import Refund


def create_refund(booking, refund_percentage, refund_amount):

    refund = Refund.objects.create(
        booking=booking,
        refund_percentage=refund_percentage,
        refund_amount=refund_amount,
        payment_method=getattr(booking.payment, "method", ""),
        refund_account=""
    )

    # SEND EMAIL TO ADMIN (NO EXTRA APP NEEDED)
    send_mail(
        subject="Refund Request",
        message=f"""
Refund Request

Booking ID: {booking.id}
Customer: {booking.user.email}

Refund Amount: Rs {refund_amount}
Refund Percentage: {refund_percentage}%

Payment Method: {refund.payment_method}
Refund Account: {refund.refund_account}
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["admin@example.com"]
    )

    return refund