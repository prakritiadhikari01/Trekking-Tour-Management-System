from django.urls import path

from trekking_and_tour_management_system.guides.api.views import (
    GuideDashboardAPIView,
)

urlpatterns = [
    path(
        "dashboard/",
        GuideDashboardAPIView.as_view(),
        name="guide-dashboard",
    ),
]