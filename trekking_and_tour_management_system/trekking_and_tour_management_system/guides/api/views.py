from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trekking_and_tour_management_system.guides.services.guide_services import create_guide_by_admin
from trekking_and_tour_management_system.users.permissions import IsGuide
from trekking_and_tour_management_system.bookings.models import Booking
from users.permissions import IsGuide


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .serializers import GuideCreateSerializer


class CreateGuideAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data

        guide = create_guide_by_admin(
            email=data["email"],
            full_name=data["full_name"],
            phone_number=data["phone_number"],
            experience=data["experience"],
            languages=data["languages"]
        )

        return Response(
            {"message": "Guide created successfully"},
            status=201
        )
    
class GuideDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsGuide
    ]

    def get(self, request):

        return Response({
            "message": "Welcome Guide",
            "assigned_tours": [],
        
        })
    

class GuideAssignedToursAPIView(APIView):

    def get(self, request):

        bookings = Booking.objects.filter(
            assigned_guide__user=request.user
        ).select_related("package", "user")

        data = []

        for b in bookings:
            data.append({
                "id": b.id,
                "package": b.package.title,
                "destination": b.package.destination,
                "customer": b.full_name,
                "start": b.trip_start_date,
                "end": b.trip_end_date,
                "status": b.guide_status,
                "booking_status": b.booking_status,
                "assigned_at": b.guide_assigned_at,
            })

        return Response(data)
    
class GuideRespondAssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsGuide]

    def post(self, request, booking_id):

        action = request.data.get("action")

        booking = Booking.objects.get(
            id=booking_id,
            assigned_guide__user=request.user
        )

        if action == "accept":
            booking.guide_status = "ACCEPTED"
            booking.booking_status = "ONGOING"

        elif action == "reject":
            booking.guide_status = "REJECTED"
            booking.assigned_guide = None

        booking.save()

        return Response({"status": booking.guide_status})