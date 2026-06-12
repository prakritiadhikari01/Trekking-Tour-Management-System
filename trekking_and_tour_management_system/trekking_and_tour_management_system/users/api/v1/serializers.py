from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from trekking_and_tour_management_system.users.models import User
from trekking_and_tour_management_system.users.services.user_service import (
    UserService,
)


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
        fields = [
            "name",
            "email",
            "password",
        ]

    def create(self, validated_data):

        return UserService.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        user = authenticate(
            email=attrs["email"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        attrs["user"] = user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()

    def validate(self, attrs):

        user = self.context["user"]

        if not user.check_password(
            attrs["old_password"]
        ):
            raise serializers.ValidationError(
                {
                    "old_password":
                    "Old password is incorrect."
                }
            )

        if (
            attrs["new_password"]
            != attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        return attrs

    def save(self):

        user = self.context["user"]

        user.set_password(
            self.validated_data["new_password"]
        )

        user.must_change_password = False

        user.save()

        return user


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()


class PasswordResetConfirmSerializer(
    serializers.Serializer
):

    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )

    confirm_password = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        if (
            attrs["password"]
            != attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        uidb64 = self.context["uidb64"]
        token = self.context["token"]

        try:

            uid = (
                urlsafe_base64_decode(uidb64)
                .decode()
            )

            user = User.objects.get(pk=uid)

        except (
            User.DoesNotExist,
            Exception,
        ):
            raise serializers.ValidationError(
                "Invalid reset link."
            )

        if not PasswordResetTokenGenerator().check_token(
            user,
            token,
        ):
            raise serializers.ValidationError(
                "Invalid or expired token."
            )

        attrs["user"] = user

        return attrs

    def save(self):

        user = self.validated_data["user"]

        user.set_password(
            self.validated_data["password"]
        )

        user.must_change_password = False

        user.save()

        return user