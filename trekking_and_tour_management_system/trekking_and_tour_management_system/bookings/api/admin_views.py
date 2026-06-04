from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



from trekking_and_tour_management_system.users.permissions import IsAdmin
from trekking_and_tour_management_system.bookings.services.guide_assignment_service import (
    GuideAssignmentService,
)

class AssignGuideAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def post(self, request, booking_id):

        guide_id = request.data.get("guide_id")

        GuideAssignmentService.assign_guide(
            booking_id=booking_id,
            guide_id=guide_id,
        )

        return Response({
            "message": "Guide assigned successfully."
        })