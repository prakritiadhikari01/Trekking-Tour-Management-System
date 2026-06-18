from reports.selectors.booking_selector import get_revenue, get_total_bookings


class RevenueReportService:

    def build(self):
        revenue_data = get_revenue()

        return {
            "total_revenue": revenue_data.get("total", 0),
            "total_bookings": get_total_bookings(),
        }