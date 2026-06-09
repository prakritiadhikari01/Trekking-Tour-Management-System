from django.urls import path
from reports.api.views import (
    BookingReportView,
    CustomerReportAPIView,
    DashboardAnalyticsView,
    PackageReportAPIView,
    RevenueReportView
)

urlpatterns = [
    path("bookings/", BookingReportView.as_view(), name="booking-report"),
    path("revenue/", RevenueReportView.as_view(), name="revenue-report"),
    path("dashboard/", DashboardAnalyticsView.as_view(), name="dashboard-analytics"),
    path("customers/",CustomerReportAPIView.as_view(),name="customer-report"),
    path("packages/",PackageReportAPIView.as_view(),name="package-report"),
]