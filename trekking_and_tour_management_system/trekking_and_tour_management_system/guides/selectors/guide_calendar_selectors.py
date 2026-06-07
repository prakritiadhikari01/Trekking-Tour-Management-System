from trekking_and_tour_management_system.bookings.models import Booking


def get_guide_calendar(guide):
    return (
        Booking.objects
        .filter(
            assigned_guide=guide,
            guide_status__in=[
                "PENDING",
                "ACCEPTED",
            ]
        )
        .order_by("trip_start_date")
    )