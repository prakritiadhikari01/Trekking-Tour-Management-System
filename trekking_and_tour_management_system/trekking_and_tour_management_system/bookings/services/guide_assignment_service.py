# bookings/guide_assignment_service.py

from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from trekking_and_tour_management_system.bookings.services.customer_email_service import (
    send_customer_accept_email,
)

from trekking_and_tour_management_system.bookings.services.guide_email_service import (
    send_admin_notification_email,
)
from trekking_and_tour_management_system.bookings.selectors.booking_selectors import (
    get_booking_by_id,
    get_guide_booking,
)

from trekking_and_tour_management_system.guides.selectors.guide_selectors import (
    get_guide_by_id,
)


class GuideAssignmentService:
    @staticmethod
    def assign_guide(
        booking_id,
        guide_id,
    ):
        booking = get_booking_by_id(
            booking_id
        )

        guide = get_guide_by_id(
            guide_id
        )

        booking.assigned_guide = guide
        booking.guide_status = "PENDING"
        booking.guide_assigned_at = timezone.now()

        booking.save()

        return booking
    
    @staticmethod
    def respond_to_assignment(
        booking_id,
        guide_user,
        action,
    ):

        try:

            booking = get_guide_booking(
                booking_id=booking_id,
                guide_user=guide_user,
            )

        except ObjectDoesNotExist:

            raise ValueError(
                "Booking not found"
            )

        if action not in [
            "accept",
            "reject",
        ]:
            raise ValueError(
                "Invalid action"
            )

        if action == "accept":

            booking.guide_status = "ACCEPTED"
            booking.booking_status = "ONGOING"

        else:

            booking.guide_status = "REJECTED"

        booking.save()

        if action == "accept":
            send_customer_accept_email(
                booking
            )

        send_admin_notification_email(
            booking
        )

        return booking
    
