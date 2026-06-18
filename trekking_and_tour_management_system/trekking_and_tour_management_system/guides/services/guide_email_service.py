# bookings/services/guide_email_service.py

from django.core.mail import send_mail
from django.conf import settings

from trekking_and_tour_management_system.core.services.email_service import EmailService


def send_guide_assignment_email(booking):
    print("Sending guide assignment email...")
    guide = booking.assigned_guide
    info = booking.package.info

    EmailService.send_plain_maill(
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



def send_guide_account_ready_email(user, reset_link):
    print(f"Sending guide account ready email to {user.email}...")
    print(f"Reset link: {reset_link}")
    send_mail(
        subject="Your Guide Account is Ready",
        message=f"""Hi {user.name},
Your guide account has been created.
Set your password using this link:
{reset_link}
After setting password, you can log in using your email.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )