from django.db.models import Count, Sum
from trekking_and_tour_management_system.bookings.models import Booking


def get_total_bookings():
    return Booking.objects.count()


def get_revenue():
    return Booking.objects.aggregate(total=Sum("payment__amount"))


def get_booking_by_user():
    return (
        Booking.objects.values(
            "user__id",
            "user__name",
            "user__email",
        )
        .annotate(total_bookings=Count("id"))
    )