from django.urls import path

from trekking_and_tour_management_system.guides.api.views import (
    CreateGuideAPIView,
    GuideAssignedToursAPIView,
    GuideDashboardAPIView,
    GuideRespondAssignmentAPIView,
)

urlpatterns = [
    path(
        "dashboard/",
        GuideDashboardAPIView.as_view(),
        name="guide-dashboard",
    ),
    path("create/", CreateGuideAPIView.as_view(), name="create-guide"),
    path(
    "assignments/",
    GuideAssignedToursAPIView.as_view(),
),

path(
    "assignments/<int:booking_id>/respond/",
    GuideRespondAssignmentAPIView.as_view(),
),
]