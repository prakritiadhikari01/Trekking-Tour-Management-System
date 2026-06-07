# guides/selectors/guide_assignment_selectors.py
from trekking_and_tour_management_system.bookings.models import Booking


def get_booking_for_assignment(booking_id):
    """
    Used by admin when assigning a guide.
    """
    return (
        Booking.objects
        .select_related(
            "package",
            "user",
            "assigned_guide",
        )
        .get(id=booking_id)
    )


def get_guide_assigned_bookings(guide_user):
    """
    Returns all bookings assigned to a guide.
    Used in guide dashboard.
    """
    return (
        Booking.objects
        .filter(
            assigned_guide__user=guide_user
        )
        .select_related(
            "package",
            "user",
            "assigned_guide",
        )
    )


def get_guide_booking(
    booking_id,
    guide_user,
):
    """
    Returns a specific booking belonging
    to the currently logged-in guide.
    """
    return (
        Booking.objects
        .select_related(
            "package",
            "user",
            "assigned_guide",
        )
        .get(
            id=booking_id,
            assigned_guide__user=guide_user,
        )
    )


def get_pending_guide_assignments():
    """
    Admin dashboard helper.
    Shows bookings waiting for guide response.
    """
    return (
        Booking.objects
        .filter(
            assigned_guide__isnull=False,
            guide_status="PENDING",
        )
        .select_related(
            "package",
            "user",
            "assigned_guide",
        )
    )


def get_accepted_guide_assignments():
    return (
        Booking.objects
        .filter(
            guide_status="ACCEPTED",
        )
        .select_related(
            "package",
            "user",
            "assigned_guide",
        )
    )


def get_rejected_guide_assignments():
    return (
        Booking.objects
        .filter(
            guide_status="REJECTED",
        )
        .select_related(
            "package",
            "user",
            "assigned_guide",
        )
    )