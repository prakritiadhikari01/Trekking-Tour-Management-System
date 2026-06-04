from django.urls import path

from trekking_and_tour_management_system.users.api.views.auth_views import (
    RegisterAPIView,
    LoginAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]