from rest_framework.routers import DefaultRouter

from django.urls import path

from trekking_and_tour_management_system.users.api.views.auth_views import RegisterAPIView, LoginAPIView, ChangePasswordAPIView, LogoutAPIView, PasswordResetConfirmView
from trekking_and_tour_management_system.users.api.views.views import UserViewSet



router = DefaultRouter()
router.include_format_suffixes = False
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls + [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm"
    ),]

