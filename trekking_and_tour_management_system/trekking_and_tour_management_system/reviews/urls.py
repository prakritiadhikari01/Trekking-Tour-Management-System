# from rest_framework.routers import DefaultRouter
# from .api.v1.views import ReviewViewSet

# router = DefaultRouter()
# router.register(r"reviews", ReviewViewSet, basename="reviews")

# urlpatterns = router.urls
# reviews/urls.py

from rest_framework.routers import DefaultRouter
from .api.v1.views import ReviewViewSet

router = DefaultRouter()
router.register(
    r"reviews",
    ReviewViewSet,
    basename="review"
)

urlpatterns = router.urls