from rest_framework import serializers

from trekking_and_tour_management_system.guide_applications.models import GuideApplication

class GuideApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuideApplication

        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "experience",
            "languages",
            "cv",
            "citizenship_document",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "status",
            "created_at",
        ]

    def validate_email(self, value):

        if GuideApplication.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Application with this email already exists."
            )

        return value