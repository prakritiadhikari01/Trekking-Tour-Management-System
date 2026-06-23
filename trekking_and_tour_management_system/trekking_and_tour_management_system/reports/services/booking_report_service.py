# trekking_and_tour_management_system/reports/services/booking_report_service.py

from ..selectors.booking_selector import (
    get_bookings,
    get_revenue,
)


def generate_booking_report(
    start_date=None,
    end_date=None,
    status=None,
):
    """
    Generate booking statistics and booking list.
    """

    bookings = get_bookings(
        start_date=start_date,
        end_date=end_date,
        status=status,
    )

    return {
        "total_bookings": bookings.count(),
        "confirmed": bookings.filter(
            booking_status="CONFIRMED"
        ).count(),
        "pending": bookings.filter(
            booking_status="PENDING"
        ).count(),
        "cancelled": bookings.filter(
            booking_status="CANCELLED"
        ).count(),
        "data": [
            {
                "id": booking.id,
                #"user": getattr(booking.user, "username", str(booking.user)),
                "user": booking.email,
                "package": str(booking.package),
                "status": booking.booking_status,
                "price": booking.total_price,
                "date": booking.created_at,
            }
            for booking in bookings
        ],
    }


def generate_revenue_report(
    start_date=None,
    end_date=None,
):
    """
    Generate revenue report.
    """

    revenue_data = get_revenue(
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "total_revenue": revenue_data.get(
            "total_revenue",
            0,
        )
        or 0
    }