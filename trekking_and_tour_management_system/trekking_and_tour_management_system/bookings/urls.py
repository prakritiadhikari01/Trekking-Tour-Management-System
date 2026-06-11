from django.urls import path
from .api.views import (
    BookingListCreateAPIView,
    BookingDetailAPIView,
    BookingHistoryView,
    CancelBookingAPIView,
)

from trekking_and_tour_management_system.guides.api.admin_views import AssignGuideAPIView

urlpatterns = [
    path("", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDetailAPIView.as_view(), name="booking-detail"),
    path("history/", BookingHistoryView.as_view(), name="booking-history"),
    path("<int:pk>/cancel/", CancelBookingAPIView.as_view(), name="booking-cancel"),

    path(
        "<int:booking_id>/assign-guide/",
        AssignGuideAPIView.as_view(),
        name="assign-guide",
    ),
]