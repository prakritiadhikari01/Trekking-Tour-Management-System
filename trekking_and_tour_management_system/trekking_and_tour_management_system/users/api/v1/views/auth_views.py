from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework_simplejwt.tokens import (
    RefreshToken,
)

from drf_spectacular.utils import extend_schema

from trekking_and_tour_management_system.users.api.v1.serializers import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        refresh = RefreshToken.for_user(
            user
        )

        return Response(
            {
                "message":
                "User registered successfully",
                "refresh": str(refresh),
                "access": str(
                    refresh.access_token
                ),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    request=LoginSerializer,
)
class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data[
            "user"
        ]

        refresh = RefreshToken.for_user(
            user
        )

        if user.role == "guide":
            dashboard = "guide-dashboard"

        elif user.role == "admin":
            dashboard = "admin-dashboard"

        else:
            dashboard = "customer-dashboard"

        return Response(
            {
                "message":
                "Login successful",
                "refresh": str(refresh),
                "access": str(
                    refresh.access_token
                ),
                "dashboard": dashboard,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "must_change_password":
                    user.must_change_password,
                },
            }
        )


class ChangePasswordAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = (
            ChangePasswordSerializer(
                data=request.data,
                context={
                    "user": request.user
                },
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message":
                "Password changed successfully"
            }
        )


class LogoutAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        refresh_token = (
            serializer.validated_data[
                "refresh"
            ]
        )

        try:

            token = RefreshToken(
                refresh_token
            )

            token.blacklist()

        except Exception:

            return Response(
                {
                    "error":
                    "Invalid refresh token"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message":
                "Logout successful"
            }
        )


class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(
        self,
        request,
        uidb64,
        token,
    ):

        serializer = (
            PasswordResetConfirmSerializer(
                data=request.data,
                context={
                    "uidb64": uidb64,
                    "token": token,
                },
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message":
                "Password reset successful"
            }
        )