# guide_conflict_selectors.py
from trekking_and_tour_management_system.bookings.models import Booking


def has_guide_date_conflict(
    guide,
    start_date,
    end_date,
):
    return Booking.objects.filter(
        assigned_guide=guide,
        guide_status__in=[
            "PENDING",
            "ACCEPTED",
        ],
        trip_start_date__lte=end_date,
        trip_end_date__gte=start_date,
    ).exists()