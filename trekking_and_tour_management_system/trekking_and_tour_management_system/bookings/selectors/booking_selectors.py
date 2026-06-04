from trekking_and_tour_management_system.bookings.models import Booking


def get_booking_by_id(
    booking_id,
):
    return Booking.objects.select_related(
        "package",
        "user",
        "assigned_guide",
    ).get(
        id=booking_id
    )


def get_guide_booking(
    booking_id,
    guide_user,
):
    return Booking.objects.get(
        id=booking_id,
        assigned_guide__user=guide_user,
    )

def get_guide_assigned_bookings(
    guide_user,
):
    return (
        Booking.objects.filter(
            assigned_guide__user=guide_user
        )
        .select_related(
            "package",
            "user",
        )
    )