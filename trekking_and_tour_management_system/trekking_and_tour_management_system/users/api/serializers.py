from rest_framework import serializers
from trekking_and_tour_management_system.users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "role",
        ]
        read_only_fields = ["role"]

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def create(self, validated_data):

        user = User.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
            role="customer"
        )

        return user
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        attrs["user"] = user

        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(required=True)
