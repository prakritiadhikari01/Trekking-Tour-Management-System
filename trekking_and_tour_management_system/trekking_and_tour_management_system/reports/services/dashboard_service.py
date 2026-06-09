from reports.selectors.dashboard_selector import *


def get_dashboard_data():
    revenue = get_total_revenue()

    return {
        "bookings": {
            "total": get_total_bookings(),
            "confirmed": get_confirmed_bookings(),
            "pending": get_pending_bookings(),
            "cancelled": get_cancelled_bookings(),
        },
        "revenue": {
            "total": revenue["revenue"] or 0
        },
        "customers": {
            "total": get_total_customers()
        },
        "packages": {
            "total": get_total_packages()
        }
    }