from rest_framework.routers import DefaultRouter
from trekking_and_tour_management_system.packages.api.v1.views import TrekPackageViewSet

router = DefaultRouter()
router.include_format_suffixes = False
router.register(r"packages", TrekPackageViewSet, basename="packages")

urlpatterns = router.urls