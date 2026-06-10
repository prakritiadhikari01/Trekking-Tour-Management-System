from reports.selectors.booking_selector import (
    get_total_bookings,
    get_revenue,
    get_booking_by_user,
)

from reports.selectors.customer_selector import (
    get_total_customers,
    get_active_customers,
)

from reports.selectors.package_selector import get_top_packages


class DashboardService:

    def build(self):
        revenue_data = get_revenue()

        return {
            "total_customers": get_total_customers(),
            "active_customers": get_active_customers(),
            "total_bookings": get_total_bookings(),
            "total_revenue": revenue_data["total"] or 0,
            "top_customers": list(get_booking_by_user())[:5],
            "top_packages": list(get_top_packages())[:5],
        }