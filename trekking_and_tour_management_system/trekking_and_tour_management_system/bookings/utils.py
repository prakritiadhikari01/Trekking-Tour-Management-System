from django.utils import timezone
from django.db import transaction

from trekking_and_tour_management_system.payments.models import Payment, Refund
from trekking_and_tour_management_system.bookings.models import Booking


# -------------------------------
# REFUND LOGIC (DAY BASED POLICY)
# -------------------------------

def calculate_refund_percentage(trek_date):

    days_left = (trek_date - timezone.now().date()).days

    if days_left >= 30:
        return 100
    elif days_left >= 15:
        return 50
    else:
        return 0


# -------------------------------
# CREATE CANCELLATION REQUEST
# -------------------------------

@transaction.atomic
def create_cancellation_request(booking, user, reason):

    refund_percentage = calculate_refund_percentage(
        booking.package.start_date
    )

    refund_amount = (booking.total_amount * refund_percentage) / 100

    cancellation = CancellationRequest.objects.create(
        booking=booking,
        user=user,
        reason=reason,
        refund_amount=refund_amount,
        status="PENDING"
    )

    return cancellation


# -------------------------------
# APPROVE CANCELLATION (ADMIN)
# -------------------------------

@transaction.atomic
def approve_cancellation(cancellation):

    booking = cancellation.booking
    payment = Payment.objects.filter(booking=booking).first()

    booking.booking_status = "CANCELLED"
    booking.cancellation_reason = cancellation.reason
    booking.cancelled_at = timezone.now()

    booking.save()

    # mark payment failed/closed
    if payment:
        payment.status = "FAILED"
        payment.save(update_fields=["status"])

    # create refund record
    refund = Refund.objects.create(
        booking=booking,
        payment=payment,
        amount=cancellation.refund_amount,
        status="PENDING"
    )

    cancellation.status = "APPROVED"
    cancellation.save()

    return refund


# -------------------------------
# REJECT CANCELLATION
# -------------------------------

def reject_cancellation(cancellation):
    cancellation.status = "REJECTED"
    cancellation.save()