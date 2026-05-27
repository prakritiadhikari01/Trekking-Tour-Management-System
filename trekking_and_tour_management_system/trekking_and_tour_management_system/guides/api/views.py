from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trekking_and_tour_management_system.guides.services.guide_services import send_customer_trip_details
from trekking_and_tour_management_system.users.permissions import IsGuide
from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.bookings.guide_assignment_service import assign_guide_to_booking



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
    permission_classes = [IsAuthenticated, IsGuide]

    def get(self, request):

        bookings = Booking.objects.filter(
            assigned_guide__user=request.user
        ).select_related("package", "user")

        data = []

        for b in bookings:
            data.append({
                "booking_id": b.id,
                "customer": b.full_name,
                "package": b.package.title,
                "start": b.trip_start_date,
                "end": b.trip_end_date,
                "status": b.guide_status,
                "booking_status": b.booking_status,
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

            # trigger celery/email here
            send_customer_trip_details(booking)

        elif action == "reject":
            booking.guide_status = "REJECTED"
            booking.assigned_guide = None

        booking.save()

        return Response({"status": booking.guide_status})