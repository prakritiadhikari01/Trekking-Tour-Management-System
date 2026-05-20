from django.urls import path

from trekking_and_tour_management_system.users.api.auth_views import LoginAPIView, RegisterAPIView

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
