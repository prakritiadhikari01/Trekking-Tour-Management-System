from django.db import transaction
from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.guides.models import Guide


@transaction.atomic
def assign_guide_to_booking(booking: Booking, guide: Guide):

    if booking.assigned_guide:
        raise Exception("Guide already assigned")

    booking.assigned_guide = guide

    # keep status as CONFIRMED (payment done state)
    if booking.booking_status == "PENDING":
        booking.booking_status = "CONFIRMED"

    booking.save()

    return booking