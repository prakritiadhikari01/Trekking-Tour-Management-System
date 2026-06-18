from django.urls import path

from trekking_and_tour_management_system.guide_applications.api.views import (
    GuideApplicationCreateAPIView,
)

urlpatterns = [
    path(
        "apply/",
        GuideApplicationCreateAPIView.as_view(),
        name="guide-application",
    ),
]