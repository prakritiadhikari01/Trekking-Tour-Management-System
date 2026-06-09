from reports.selectors.booking_selector import (
    get_bookings,
    get_revenue
)


def generate_booking_report(start_date=None, end_date=None, status=None):
    bookings = get_bookings(start_date, end_date, status)

    total = bookings.count()
    confirmed = bookings.filter(booking_status="CONFIRMED").count()
    pending = bookings.filter(booking_status="PENDING").count()
    cancelled = bookings.filter(booking_status="CANCELLED").count()

    return {
        "total_bookings": total,
        "confirmed": confirmed,
        "pending": pending,
        "cancelled": cancelled,
        "data": [
            {
                "id": b.id,
                "user": b.user.username,
                "package": str(b.package),
                "status": b.booking_status,
                "price": b.total_price,
                "date": b.created_at
            }
            for b in bookings
        ]
    }

def generate_revenue_report(start_date=None, end_date=None):
    revenue_data = get_revenue(start_date, end_date)

    return {
        "total_revenue": revenue_data["total_revenue"] or 0
    }