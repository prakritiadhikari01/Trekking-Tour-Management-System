from rest_framework.routers import DefaultRouter

from trekking_and_tour_management_system.users.api.views import ContactSupportCreateView, UserViewSet
from django.urls import path

from .auth_views import ChangePasswordAPIView, LogoutAPIView, RegisterAPIView
from .auth_views import LoginAPIView


router = DefaultRouter()
router.include_format_suffixes = False
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls + [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("support/contact/", ContactSupportCreateView.as_view(), name="contact-support"),
]
