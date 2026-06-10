#app/guides/selectors/guide_availability_selectors.py
from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.guides.models import Guide


def get_available_guides_for_booking(
    booking,
):
    busy_guide_ids = (
        Booking.objects.filter(
            assigned_guide__isnull=False,
            guide_status__in=[
                "PENDING",
                "ACCEPTED",
            ],
            trip_start_date__lte=booking.trip_end_date,
            trip_end_date__gte=booking.trip_start_date,
        )
        .values_list(
            "assigned_guide_id",
            flat=True,
        )
    )

    return (
        Guide.objects.filter(
            is_verified=True,
        )
        .exclude(
            id__in=busy_guide_ids,
        )
        .select_related(
            "user"
        )
    )