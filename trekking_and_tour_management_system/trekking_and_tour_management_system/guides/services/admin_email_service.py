from trekking_and_tour_management_system.core.services.email_services import (
    send_plain_email,
)


def send_admin_notification_email(booking):
    print("Sending admin notification email about guide response...")

    send_plain_email(
        subject="Guide Responded to Assignment",
        message=f"""
Hello Admin,

The guide {booking.assigned_guide.full_name} has responded to the assignment.

Booking ID: {booking.id}
Guide Status: {booking.guide_status}
Booking Status: {booking.booking_status}

Please review the booking and take necessary actions.
""",
        recipients=[],
    )