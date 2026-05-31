from django.urls import path

from trekking_and_tour_management_system.guides.api.views import (
    CreateGuideAPIView,
    GuideDashboardAPIView,
)

urlpatterns = [
    path(
        "dashboard/",
        GuideDashboardAPIView.as_view(),
        name="guide-dashboard",
    ),
    path("create/", CreateGuideAPIView.as_view(), name="create-guide"),
]