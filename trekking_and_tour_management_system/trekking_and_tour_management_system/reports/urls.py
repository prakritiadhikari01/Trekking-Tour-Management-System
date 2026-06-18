from django.urls import path
from trekking_and_tour_management_system.reports.api.views import (
    BookingExcelExportView,
    CustomerReportAPIView,
    PackageReportAPIView,
    RevenueExportPDFView,
    RevenueReportAPIView,
    DashboardAPIView,
    BookingReportAPIView,
    download_report,
)

urlpatterns = [
    path("customers/", CustomerReportAPIView.as_view()),
    path("packages/", PackageReportAPIView.as_view()),
    path("revenue/", RevenueReportAPIView.as_view()),
    path("dashboard/", DashboardAPIView.as_view()),
    path("bookings/", BookingReportAPIView.as_view()),
    path("revenue/export-pdf/", RevenueExportPDFView.as_view(), name="revenue-export-pdf"),
    path("download/", download_report, name="download_report"),
    path(
    "export/excel/",
    BookingExcelExportView.as_view(),
    name="booking-excel-export",
),
    
]