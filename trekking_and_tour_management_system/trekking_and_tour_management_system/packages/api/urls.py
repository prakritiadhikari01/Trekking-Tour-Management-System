from rest_framework.routers import DefaultRouter

from trekking_and_tour_management_system.packages.api.views import (
    TrekPackageViewSet,
)

router = DefaultRouter()

router.register(
    r"packages",
    TrekPackageViewSet,
    basename="packages",
)

urlpatterns = router.urls