from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import LoginSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()


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
                "role": user.role
            }
        })