#guides/api/serializers.py
from rest_framework import serializers

from trekking_and_tour_management_system.guides.models import Guide


class GuideCreateSerializer(serializers.Serializer):

    email = serializers.EmailField()

    full_name = serializers.CharField(
        max_length=255
    )

    phone_number = serializers.CharField(
        max_length=20
    )

    experience = serializers.CharField()

    languages = serializers.CharField()


class GuideSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:

        model = Guide

        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "experience",
            "languages",
            "is_verified",
        ]