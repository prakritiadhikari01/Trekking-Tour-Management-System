from django.urls import path
from .views import BookingListCreateAPIView, BookingDetailAPIView

urlpatterns = [
    path("", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDetailAPIView.as_view(), name="booking-detail"),
]