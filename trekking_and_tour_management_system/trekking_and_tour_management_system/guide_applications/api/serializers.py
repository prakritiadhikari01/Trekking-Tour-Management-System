from rest_framework import serializers

from trekking_and_tour_management_system.guide_applications.models import GuideApplication


class GuideApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuideApplication
        fields = [
            "id",
            "user",
            "portfolio_link",
            "experience",
            "status",
            "admin_note",
            "created_at",
        ]
        read_only_fields = ["user", "status", "admin_note"]