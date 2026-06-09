from reports.selectors.package_selector import get_top_packages
from reports.selectors.booking_selector import get_total_bookings


class PackageReportService:

    def build(self):
        return {
            "total_bookings": get_total_bookings(),
            "top_packages": list(get_top_packages()),
        }