from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from trekking_and_tour_management_system.packages.api.views import TrekPackageViewSet
from trekking_and_tour_management_system.users.api.views import UserViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# register ALL API viewsets here
router.register(r"users", UserViewSet, basename="users")
router.register(r"packages", TrekPackageViewSet, basename="packages")

app_name = "api"

urlpatterns = router.urls