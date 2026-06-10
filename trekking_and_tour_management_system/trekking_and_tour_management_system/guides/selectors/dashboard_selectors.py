#guides/selectors/dashboard_selectors.py

from trekking_and_tour_management_system.guides.selectors.guide_assignment_selectors import get_guide_assigned_bookings

def get_guide_dashboard_data(user):
    bookings = get_guide_assigned_bookings(user)

    return [
        {
            "id": booking.id,
            "package": booking.package.title,
            "destination": booking.package.destination,
            "customer": booking.full_name,
            "start": booking.trip_start_date,
            "end": booking.trip_end_date,
            "status": booking.guide_status,
            "booking_status": booking.booking_status,
            "assigned_at": booking.guide_assigned_at,
        }
        for booking in bookings
    ]