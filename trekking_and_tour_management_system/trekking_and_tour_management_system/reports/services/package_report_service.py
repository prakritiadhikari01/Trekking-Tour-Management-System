from django.db.models import Count

from trekking_and_tour_management_system.bookings.models import Booking
from reports.selectors.booking_selector import Booking

def generate_package_report():

    top_packages = (
        Booking.objects.values(
            "package__id",
            "package__title"
        )
        .annotate(
            total_bookings=Count("id")
        )
        .order_by("-total_bookings")[:10]
    )

    return {
        "top_packages": list(top_packages)
    }