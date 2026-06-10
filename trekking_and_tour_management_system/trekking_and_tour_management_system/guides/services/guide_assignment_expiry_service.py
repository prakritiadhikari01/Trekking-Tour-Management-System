#guides/services/guide_assignment_expiry_service.py
from django.utils import timezone

from trekking_and_tour_management_system.bookings.models import Booking


class GuideAssignmentExpiryService:

    @staticmethod
    def expire_pending_assignments():

        expired_bookings = Booking.objects.filter(
            guide_status="PENDING",
            guide_response_deadline__lt=timezone.now(),
        )

        count = expired_bookings.update(
            guide_status="EXPIRED",
            assigned_guide=None,
        )

        return count