from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "customer")

        if not name or not email or not password:
            return Response(
                {"error": "name, email, password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            name=name,
            email=email,
            role=role,
            password=make_password(password)
        )
        

        return Response(
            {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED
        )
    
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "role": user.role
            }
        })