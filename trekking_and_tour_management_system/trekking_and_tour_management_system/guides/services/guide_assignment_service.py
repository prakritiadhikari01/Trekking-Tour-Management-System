# guides/services/guide_assignment_service.py

from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.guides.selectors.guide_assignment_selectors import (
    get_booking_for_assignment,
    get_guide_booking,
)

from trekking_and_tour_management_system.guides.selectors.guide_selectors import (
    get_guide_by_id,
)
from trekking_and_tour_management_system.guides.tasks import send_admin_notification_email_task, send_customer_accept_email_task


class GuideAssignmentService:
    @staticmethod
    def assign_guide(
        booking_id,
        guide_id,
    ):
        booking = get_booking_for_assignment(
            booking_id
        )

        guide = get_guide_by_id(
            guide_id
        )

        busy_booking_exists = (
            Booking.objects.filter(
                assigned_guide=guide,
                guide_status__in=[
                    "PENDING",
                    "ACCEPTED",
                ],
                trip_start_date__lte=booking.trip_end_date,
                trip_end_date__gte=booking.trip_start_date,
            )
            .exists()
        )

        if busy_booking_exists:
            raise ValueError(
                "Guide is not available for selected dates."
            )

        booking.assigned_guide = guide
        booking.guide_status = "PENDING"
        booking.guide_assigned_at = timezone.now()

        booking.guide_response_deadline = (
            timezone.now()
            + timezone.timedelta(hours=24)
        )

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

        if booking.guide_status == "EXPIRED":
            raise ValueError(
                "Assignment expired"
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
            booking.guide_response_deadline = None

        else:

            booking.guide_status = "REJECTED"
            booking.guide_response_deadline = None

        booking.save()

        if action == "accept":

            send_customer_accept_email_task.delay(
                booking.id
            )

        send_admin_notification_email_task.delay(
            booking.id
        )

        return booking