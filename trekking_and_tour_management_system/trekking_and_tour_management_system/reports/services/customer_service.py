from reports.selectors.customer_selector import (
    get_total_customers,
    get_active_customers,
)
from reports.selectors.booking_selector import get_booking_by_user


class CustomerReportService:

    def build(self):
        return {
            "total_customers": get_total_customers(),
            "active_customers": get_active_customers(),
            "top_customers": list(get_booking_by_user()),
        }