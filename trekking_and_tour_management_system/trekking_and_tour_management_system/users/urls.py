from django.urls import path
from trekking_and_tour_management_system.users.api.v1.views.auth_views import (
    RegisterAPIView,
    LoginAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
    PasswordResetConfirmView,
)
from trekking_and_tour_management_system.users.api.v1.views.user_views import UserViewSet

app_name = "users"

urlpatterns = [
    
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),

    # profile endpoint (important for /me)
    path("me/", UserViewSet.as_view({"get": "me"}), name="me"),

    
]