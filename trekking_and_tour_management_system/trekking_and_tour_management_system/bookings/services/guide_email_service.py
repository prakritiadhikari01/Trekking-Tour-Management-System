# bookings/services/guide_email_service.py

from django.core.mail import send_mail
from django.conf import settings


def send_guide_assignment_email(booking):
    print("Sending guide assignment email...")
    guide = booking.assigned_guide
    info = booking.package.info

    send_mail(
        subject="New Trek Assignment",

        message=f"""
Hello {guide.full_name},

You have been assigned a trek.

PACKAGE: {booking.package.title}
DESTINATION: {booking.package.destination}
DURATION: {booking.package.duration} days

CUSTOMER:
Name: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone_number}

DATES:
Start: {booking.trip_start_date}
End: {booking.trip_end_date}

MEETING POINT:
{info.meeting_point if info else "Not set"}

REQUIRED ITEMS:
{info.required_items if info else "Not set"}

EMERGENCY CONTACT:
{info.emergency_contact if info else "Not set"}

Login and accept/reject the assignment.
""",

        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[guide.user.email],
    )

def send_admin_notification_email(booking):
    print("Sending admin notification email about guide response...")
    send_mail(
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
