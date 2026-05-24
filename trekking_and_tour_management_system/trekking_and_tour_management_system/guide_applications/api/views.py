from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from timezone_field import rest_framework

from trekking_and_tour_management_system.guide_applications.api.serializers import (
    GuideApplicationSerializer,
)

from trekking_and_tour_management_system.guide_applications.models import GuideApplication
from trekking_and_tour_management_system.guide_applications.services.guide_application_service import (
    send_application_received_email,
)
from rest_framework.permissions import AllowAny

class GuideApplicationCreateAPIView(APIView):

    permission_classes = [AllowAny]

    authentication_classes = []

    def post(self, request):

        serializer = GuideApplicationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        application = serializer.save()

        send_application_received_email(application)

        return Response(
            {
                "message": "Application submitted successfully."
            },
            status=status.HTTP_201_CREATED,
        )

class GuideApplicationViewSet(viewsets.ModelViewSet):

    queryset = GuideApplication.objects.all().order_by("-created_at")

    serializer_class = GuideApplicationSerializer

    def get_permissions(self):

        if self.action in ["create"]:
            return [AllowAny()]

        return super().get_permissions()