#trekking_and_tour_management_system/guides/services/admin_email_service.py
from django.conf import settings

from trekking_and_tour_management_system.core.services.email_service import EmailService

def send_admin_notification_email(booking):
    print("Sending admin notification email about guide response...")
    EmailService.send_plain_mail(
        subject="Guide Responded to Assignment",

        message=f"""
Hello Admin,
The guide {booking.assigned_guide.full_name} has responded to the assignment for booking ID {booking.id}.
Current Guide Status: {booking.guide_status}
Current Booking Status: {booking.booking_status}
Please review the booking and take necessary actions.
""",

        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
    )