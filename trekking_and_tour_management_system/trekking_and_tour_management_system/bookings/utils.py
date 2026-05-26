from django.utils import timezone
from datetime import datetime, timezone
from django.conf import settings
from django.core.mail import send_mail

def calculate_refund(travel_datetime, amount):
    """
    Cancellation policy:
    - >= 24 hours before trip → 100% refund
    - < 24 hours before trip → 80% refund (20% charge as fee)
    - After trip start → 0% refund
    """

    now = datetime.now(timezone.utc)

    hours_left = (travel_datetime - now).total_seconds() / 3600

    if hours_left >= 24:
        return amount  # full refund

    elif 0 < hours_left < 24:
        return amount * 0.8  # small cancellation fee (20%)

    else:
        return 0  # trip already started or missed     # no refund
    
from django.utils import timezone
from django.db import transaction

from .models import Booking, CancellationRequest, Refund
from payments.models import Payment


def calculate_refund(booking):
    """
    Simple refund logic (customize later)
    """
    if booking.travel_date > timezone.now().date():
        return float(booking.total_price) * 0.8  # 80% refund
    return 0


@transaction.atomic
def create_cancellation_request(booking, user, reason):

    refund_amount = calculate_refund(booking)

    cancellation = CancellationRequest.objects.create(
        booking=booking,
        user=user,
        reason=reason,
        refund_amount=refund_amount
    )

    return cancellation


@transaction.atomic
def approve_cancellation(cancellation):

    booking = cancellation.booking
    payment = Payment.objects.filter(booking=booking).first()

    booking.booking_status = "cancelled"
    booking.cancellation_reason = cancellation.reason
    booking.cancelled_at = timezone.now()
    booking.refund_amount = cancellation.refund_amount

    if payment:
        booking.payment_status = "refund_pending"

        Refund.objects.create(
            booking=booking,
            payment=payment,
            amount=cancellation.refund_amount,
            reason=cancellation.reason
        )

    booking.save()
    cancellation.status = "APPROVED"
    cancellation.save()


def reject_cancellation(cancellation):
    cancellation.status = "REJECTED"
    cancellation.save()