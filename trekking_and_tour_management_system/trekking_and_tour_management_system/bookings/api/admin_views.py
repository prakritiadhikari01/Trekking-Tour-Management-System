from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.bookings.services.guide_assignment_service import assign_guide_to_booking
from trekking_and_tour_management_system.guides.models import Guide
from users.permissions import IsAdmin


class AssignGuideAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def post(self, request, booking_id):

        guide_id = request.data.get("guide_id")

        booking = Booking.objects.get(id=booking_id)

        guide = Guide.objects.get(id=guide_id)

        assign_guide_to_booking(
            booking=booking,
            guide=guide
        )

        return Response({
            "message": "Guide assigned successfully."
        })