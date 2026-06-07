from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from drf_spectacular.utils import extend_schema

from trekking_and_tour_management_system.users.api.serializers import ChangePasswordSerializer, LoginSerializer, LogoutSerializer, RegisterSerializer

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RegisterAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            })

        return Response(serializer.errors, status=400)


@extend_schema(
    request=LoginSerializer,
)
class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        if user.role == "guide":

            dashboard = "guide-dashboard"

        elif user.role == "admin":

            dashboard = "admin-dashboard"

        else:

            dashboard = "customer-dashboard"


        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "dashboard": dashboard,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "must_change_password": user.must_change_password,
            }
        })

class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(old_password):

            return Response(
                {"error": "Old password incorrect"},
                status=400
            )

        user.set_password(new_password)

        user.must_change_password = False

        user.save()

        return Response({
            "message": "Password changed successfully"
        })
    
class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception:

            return Response(
                {"error": "Invalid refresh token"},
                status=400
            )

        return Response({
            "message": "Logout successful"
        })
    

class PasswordResetConfirmView(APIView):
    permission_classes = []  # IMPORTANT: public endpoint

    def post(self, request, uidb64, token):
        password = request.data.get("password")

        if not password:
            return Response({"error": "Password required"}, status=400)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        except Exception:
            return Response({"error": "Invalid link"}, status=400)

        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(password)
        user.must_change_password = False
        user.save()

        return Response({"message": "Password set successfully"})