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