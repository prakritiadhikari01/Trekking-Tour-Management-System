#guides/api/views.py
from time import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from trekking_and_tour_management_system.guides.services.guide_assignment_service import GuideAssignmentService
from trekking_and_tour_management_system.guides.selectors.dashboard_selectors import get_guide_dashboard_data
from trekking_and_tour_management_system.guides.services.guide_services import create_guide_by_admin
from trekking_and_tour_management_system.core.permissions import IsGuide
from trekking_and_tour_management_system.bookings.models import Booking

from rest_framework import request, status

from .serializers import GuideCreateSerializer


class CreateGuideAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = GuideCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        create_guide_by_admin(
            **serializer.validated_data
        )

        return Response(
            {
                "message": "Guide created successfully"
            },
            status=status.HTTP_201_CREATED
        )
    
class GuideDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsGuide
    ]

    def get(self, request):

        return Response(
            get_guide_dashboard_data(
                request.user
            )
        )
    

class GuideAssignedToursAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsGuide
    ]
    def get(self, request):

        return Response(
            get_guide_dashboard_data(
                request.user
            )
        )
    
class GuideRespondAssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsGuide]

    def post(self, request, booking_id):

        action = request.data.get("action")

        try:

            booking = GuideAssignmentService.respond_to_assignment(
                booking_id=booking_id,
                guide_user=request.user,
                action=action,
            )

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"status": booking.guide_status})