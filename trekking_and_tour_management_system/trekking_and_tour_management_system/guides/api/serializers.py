from rest_framework import serializers

from trekking_and_tour_management_system.guides.models import Guide


class GuideProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guide
        fields = [
            "id",
            "bio",
            "verified",
        ]

class GuideCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    experience = serializers.CharField()
    languages = serializers.CharField()