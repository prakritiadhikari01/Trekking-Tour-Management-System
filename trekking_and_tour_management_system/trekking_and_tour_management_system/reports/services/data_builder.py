from trekking_and_tour_management_system.bookings.models import Booking


def get_booking_report_data():
    bookings = Booking.objects.all()
    revenue = sum(b.total_price for b in bookings)
    return bookings, revenue