from trekking_and_tour_management_system.bookings.models import Booking


def get_guide_statistics(
    guide,
):
    return {
        "total_assignments": Booking.objects.filter(
            assigned_guide=guide
        ).count(),

        "accepted_assignments": Booking.objects.filter(
            assigned_guide=guide,
            guide_status="ACCEPTED",
        ).count(),

        "pending_assignments": Booking.objects.filter(
            assigned_guide=guide,
            guide_status="PENDING",
        ).count(),

        "completed_treks": Booking.objects.filter(
            assigned_guide=guide,
            booking_status="COMPLETED",
        ).count(),
    }