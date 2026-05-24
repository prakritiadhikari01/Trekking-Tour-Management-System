from rest_framework import serializers

from trekking_and_tour_management_system.guides.models import GuideProfile


class GuideProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuideProfile
        fields = [
            "id",
            "bio",
            "verified",
        ]