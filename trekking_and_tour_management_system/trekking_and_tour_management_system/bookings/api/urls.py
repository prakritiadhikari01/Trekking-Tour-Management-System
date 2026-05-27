from django.urls import path

from trekking_and_tour_management_system.bookings.api.admin_views import AssignGuideAPIView
from .views import BookingHistoryView, BookingListCreateAPIView, BookingDetailAPIView

urlpatterns = [
    path("", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDetailAPIView.as_view(), name="booking-detail"),
    path("history/", BookingHistoryView.as_view(), name="booking-history"),

    path(
        "",
        BookingListCreateAPIView.as_view()
    ),

    path(
        "<int:pk>/",
        BookingDetailAPIView.as_view()
    ),

    path(
        "history/",
        BookingHistoryView.as_view()
    ),

    path(
        "<int:booking_id>/assign-guide/",
        AssignGuideAPIView.as_view()
    ),
]