# bookings/services/customer_email_service.py

from django.core.mail import send_mail
from django.conf import settings


def send_customer_accept_email(booking):

    guide = booking.assigned_guide
    info = booking.package.info

    send_mail(
        subject="Your Trek Has Been Confirmed",

        message=f"""
Dear {booking.full_name},

Good news! Your trek has been confirmed by the guide.

GUIDE DETAILS:
Name: {guide.full_name}
Phone: {guide.phone_number}
Languages: {guide.languages}

TREK DETAILS:
Package: {booking.package.title}
Destination: {booking.package.destination}

MEETING POINT:
{info.meeting_point if info else "TBD"}

WHAT TO BRING:
{info.required_items if info else "TBD"}

EMERGENCY CONTACT:
{info.emergency_contact if info else "TBD"}

Have a safe journey!
""",

        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[booking.email],
    )