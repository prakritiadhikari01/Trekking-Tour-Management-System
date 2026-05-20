from rest_framework.routers import DefaultRouter

from trekking_and_tour_management_system.guide_applications.api.views import GuideApplicationViewSet

router = DefaultRouter()
router.register(r"", GuideApplicationViewSet, basename="guide-applications")

urlpatterns = router.urls