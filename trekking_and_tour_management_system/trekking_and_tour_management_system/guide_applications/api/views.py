from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from trekking_and_tour_management_system.guide_applications.api.serializers import GuideApplicationSerializer
from trekking_and_tour_management_system.guide_applications.models import GuideApplication
from trekking_and_tour_management_system.guide_applications.permissions import IsAdminUser
from trekking_and_tour_management_system.guide_applications.models import GuideApplication
from trekking_and_tour_management_system.guide_applications.services.guide_application_service import GuideApplicationService

class GuideApplicationViewSet(viewsets.ModelViewSet):

    serializer_class = GuideApplicationSerializer
    queryset = GuideApplication.objects.all()

    def get_permissions(self):

        if self.action in ["list", "retrieve", "update", "partial_update"]:
            return [IsAuthenticated(), IsAdminUser()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        GuideApplicationService.create_application(
            user=self.request.user,
            validated_data=serializer.validated_data
        )

    def perform_update(self, serializer):
        instance = serializer.instance
        status = self.request.data.get("status")

        if status == "approved":
            GuideApplicationService.approve_application(instance)

        elif status == "rejected":
            GuideApplicationService.reject_application(
                instance,
                self.request.data.get("admin_note")
            )