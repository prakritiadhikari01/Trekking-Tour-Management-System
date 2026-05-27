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

