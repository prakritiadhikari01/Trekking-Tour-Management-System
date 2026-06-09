from django.urls import path
from reports.api.views import (
    CustomerReportAPIView,
    PackageReportAPIView,
    RevenueReportAPIView,
    DashboardAPIView,
    BookingReportAPIView,
)

urlpatterns = [
    path("customers/", CustomerReportAPIView.as_view()),
    path("packages/", PackageReportAPIView.as_view()),
    path("revenue/", RevenueReportAPIView.as_view()),
    path("dashboard/", DashboardAPIView.as_view()),
    path("bookings/", BookingReportAPIView.as_view()),
]