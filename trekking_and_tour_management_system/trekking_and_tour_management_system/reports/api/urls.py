from django.urls import path
from reports.api.views import (
    CustomerReportAPIView,
    PackageReportAPIView,
    RevenueExportPDFView,
    RevenueReportAPIView,
    DashboardAPIView,
    BookingReportAPIView,
    download_report
)

urlpatterns = [
    path("customers/", CustomerReportAPIView.as_view()),
    path("packages/", PackageReportAPIView.as_view()),
    path("revenue/", RevenueReportAPIView.as_view()),
    path("dashboard/", DashboardAPIView.as_view()),
    path("bookings/", BookingReportAPIView.as_view()),
    path("revenue/export-pdf/", RevenueExportPDFView.as_view(), name="revenue-export-pdf"),
    path("download/", download_report, name="download_report"),
]