#app/guides/selectors/guide_availability_selectors.py
from trekking_and_tour_management_system.guides.models import Guide
from trekking_and_tour_management_system.bookings.models import Booking


def get_available_guides_for_booking(booking):
    busy_guide_ids = []

    active_bookings = Booking.objects.filter(
        assigned_guide__isnull=False,
        guide_status__in=[
            "PENDING",
            "ACCEPTED",
        ],
    ).select_related("assigned_guide")

    for assigned_booking in active_bookings:

        overlap = (
            booking.trip_start_date <= assigned_booking.trip_end_date
            and booking.trip_end_date >= assigned_booking.trip_start_date
        )

        if overlap:
            busy_guide_ids.append(
                assigned_booking.assigned_guide_id
            )

    return (
        Guide.objects.filter(
            is_verified=True,
        )
        .exclude(
            id__in=busy_guide_ids
        )
        .select_related("user")
    )