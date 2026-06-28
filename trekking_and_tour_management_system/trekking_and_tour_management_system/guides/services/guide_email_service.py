from trekking_and_tour_management_system.core.services.email_services import (
    send_plain_email,
)


def send_guide_assignment_email(booking):
    print("Sending guide assignment email...")

    guide = booking.assigned_guide
    info = booking.package.info

    send_plain_email(
        subject="New Trek Assignment",
        message=f"""
Hello {guide.full_name},

You have been assigned a new trek.

PACKAGE DETAILS
---------------
Package: {booking.package.title}
Destination: {booking.package.destination}
Duration: {booking.package.duration} days

CUSTOMER DETAILS
----------------
Name: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone_number}

TRIP DATES
----------
Start Date: {booking.trip_start_date}
End Date: {booking.trip_end_date}

MEETING POINT
-------------
{info.meeting_point if info else "Not set"}

REQUIRED ITEMS
--------------
{info.required_items if info else "Not set"}

EMERGENCY CONTACT
-----------------
{info.emergency_contact if info else "Not set"}

Please log in and accept or reject this assignment.

Thank you.
""",
        recipients=[guide.user.email],
    )


def send_guide_account_ready_email(user, reset_link):
    print(f"Sending guide account ready email to {user.email}...")
    print(f"Reset link: {reset_link}")

    send_plain_email(
        subject="Your Guide Account is Ready",
        message=f"""
Hi {user.name},

Your guide account has been created successfully.

Please set your password using the link below:

{reset_link}

After setting your password, you can log in using your email address.

Thank you.
""",
        recipients=[user.email],
    )