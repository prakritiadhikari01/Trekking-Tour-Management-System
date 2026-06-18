from django.db.models import Count, Sum

from trekking_and_tour_management_system.bookings.models import Booking


def get_bookings(
    start_date=None,
    end_date=None,
    status=None,
):
    queryset = Booking.objects.select_related(
        "user",
        "package",
    )

    if start_date:
        queryset = queryset.filter(
            created_at__date__gte=start_date
        )

    if end_date:
        queryset = queryset.filter(
            created_at__date__lte=end_date
        )

    if status:
        queryset = queryset.filter(
            booking_status=status
        )

    return queryset


def get_total_bookings():
    return Booking.objects.count()


def get_revenue(
    start_date=None,
    end_date=None,
):
    queryset = Booking.objects.all()

    if start_date:
        queryset = queryset.filter(
            created_at__date__gte=start_date
        )

    if end_date:
        queryset = queryset.filter(
            created_at__date__lte=end_date
        )

    return {
        "total_revenue": queryset.aggregate(
            total_revenue=Sum(
                "payment__amount"
            )
        )["total_revenue"]
    }


def get_booking_by_user():
    return (
        Booking.objects.values(
            "user__id",
            "user__name",
            "user__email",
        )
        .annotate(
            total_bookings=Count("id")
        )
    )