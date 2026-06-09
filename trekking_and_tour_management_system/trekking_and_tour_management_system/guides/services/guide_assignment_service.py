from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from trekking_and_tour_management_system.guides.selectors.guide_assignment_selectors import (
    get_booking_for_assignment,
    get_guide_booking,
)

from trekking_and_tour_management_system.guides.selectors.guide_selectors import (
    get_guide_by_id,
)

from trekking_and_tour_management_system.guides.selectors.guide_conflict_selectors import (
    has_guide_date_conflict,
)

from trekking_and_tour_management_system.guides.tasks import (
    send_admin_notification_email_task,
    send_customer_accept_email_task,
)


class GuideAssignmentService:

    @staticmethod
    def assign_guide(
        booking_id,
        guide_id,
    ):
        booking = get_booking_for_assignment(
            booking_id
        )

        if not booking.need_guide:
            raise ValueError(
                "This booking does not require a guide."
            )

        guide = get_guide_by_id(
            guide_id
        )

        conflict = has_guide_date_conflict(
            guide=guide,
            start_date=booking.trip_start_date,
            end_date=booking.trip_end_date,
        )

        if conflict:
            raise ValueError(
                "Guide is already assigned during these dates."
            )

        booking.assigned_guide = guide

        booking.guide_status = "PENDING"

        booking.guide_assigned_at = timezone.now()

        booking.guide_response_deadline = (
            timezone.now()
            + timezone.timedelta(hours=24)
        )

        booking.save(
            update_fields=[
                "assigned_guide",
                "guide_status",
                "guide_assigned_at",
                "guide_response_deadline",
            ]
        )

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
                "Booking not found."
            )

        if booking.guide_status == "EXPIRED":

            raise ValueError(
                "Assignment expired."
            )

        if action not in [
            "accept",
            "reject",
        ]:

            raise ValueError(
                "Invalid action."
            )

        booking.guide_responded_at = (
            timezone.now()
        )

        booking.guide_response_deadline = (
            None
        )

        if action == "accept":

            booking.guide_status = (
                "ACCEPTED"
            )

        else:

            booking.guide_status = (
                "REJECTED"
            )

        booking.save()

        if action == "accept":

            send_customer_accept_email_task.delay(
                booking.id
            )

        send_admin_notification_email_task.delay(
            booking.id
        )

        return booking