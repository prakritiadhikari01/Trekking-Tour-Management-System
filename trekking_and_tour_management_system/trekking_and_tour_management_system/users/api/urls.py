from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trekking_and_tour_management_system.users.api.views.auth_views import (
    RegisterAPIView,
    LoginAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
    PasswordResetConfirmView,
)
from trekking_and_tour_management_system.users.api.views.views import (
    ContactSupportCreateView,
    UserViewSet,
)

# Router setup
router = DefaultRouter()
router.include_format_suffixes = False
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    # router endpoints
    path("", include(router.urls)),

    # auth endpoints
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),

    # password reset
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),

    # support
    path("support/contact/", ContactSupportCreateView.as_view(), name="contact-support"),
]