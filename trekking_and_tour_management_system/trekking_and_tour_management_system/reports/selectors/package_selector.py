from django.db.models import Count
from trekking_and_tour_management_system.bookings.models import Booking


def get_top_packages():
    return (
        Booking.objects.values(
            "package__id",
            "package__title",
        )
        .annotate(total_bookings=Count("id"))
        .order_by("-total_bookings")[:10]
    )