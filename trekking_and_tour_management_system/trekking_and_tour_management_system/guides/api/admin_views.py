# guides/api/admin_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from trekking_and_tour_management_system.users.permissions import (
    IsAdmin,
)

from trekking_and_tour_management_system.guides.services.guide_assignment_service import (
    GuideAssignmentService,
)
from trekking_and_tour_management_system.guides.services.guide_availability_service import (
    GuideAvailabilityService,
)


class AssignGuideAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    def post(self, request, booking_id):

        guide_id = request.data.get(
            "guide_id"
        )

        GuideAssignmentService.assign_guide(
            booking_id=booking_id,
            guide_id=guide_id,
        )

        return Response(
            {
                "message": "Guide assigned successfully."
            }
        )

class AvailableGuidesAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    def get(
        self,
        request,
        booking_id,
    ):
        guides = (
            GuideAvailabilityService.get_available_guides(
                booking_id
            )
        )

        return Response(
            [
                {
                    "id": guide.id,
                    "name": guide.full_name,
                    "experience": guide.experience,
                    "languages": guide.languages,
                }
                for guide in guides
            ]
        )