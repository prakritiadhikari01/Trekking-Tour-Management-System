from django.db.models import Sum
from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.users.models import User
from trekking_and_tour_management_system.packages.models import TrekPackage


def get_total_bookings():
    return Booking.objects.count()


def get_confirmed_bookings():
    return Booking.objects.filter(
        booking_status="CONFIRMED"
    ).count()


def get_pending_bookings():
    return Booking.objects.filter(
        booking_status="PENDING"
    ).count()


def get_cancelled_bookings():
    return Booking.objects.filter(
        booking_status="CANCELLED"
    ).count()


def get_total_revenue():
    return Booking.objects.filter(
        booking_status="COMPLETED"
    ).aggregate(
        revenue=Sum("total_price")
    )


def get_total_customers():
    return User.objects.count()


def get_total_packages():
    return TrekPackage.objects.count()