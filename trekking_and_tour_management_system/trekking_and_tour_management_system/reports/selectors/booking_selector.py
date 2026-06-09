from trekking_and_tour_management_system.bookings.models import Booking
from django.db.models import Sum

from trekking_and_tour_management_system.payments.models import Payment


def get_bookings(start_date=None, end_date=None, status=None):
    queryset = Booking.objects.all()

    if start_date and end_date:
        queryset = queryset.filter(created_at__range=(start_date, end_date))

    if status:
        queryset = queryset.filter(booking_status=status)

    return queryset


def get_revenue(start_date=None, end_date=None):
    queryset = Payment.objects.filter(
        status__iexact="Completed"   
    )

    if start_date and end_date:
        queryset = queryset.filter(
            created_at__range=(start_date, end_date)
        )

    result = queryset.aggregate(
        total_revenue=Sum("amount")
    )

    return result