# guides/services/customer_email_service.py
from trekking_and_tour_management_system.core.services.email_services import (
    send_plain_email,
)


def send_customer_accept_email(booking):
    print("Sending customer acceptance email...")

    guide = booking.assigned_guide
    info = booking.package.info

    send_plain_email(
        subject="Your Trek Has Been Confirmed",
        message=f"""
Dear {booking.full_name},

Good news! Your trek has been confirmed by the guide.

GUIDE DETAILS
-------------
Name: {guide.full_name}
Phone: {guide.phone_number}
Languages: {guide.languages}

TREK DETAILS
------------
Package: {booking.package.title}
Destination: {booking.package.destination}

MEETING POINT
-------------
{info.meeting_point if info else "TBD"}

WHAT TO BRING
-------------
{info.required_items if info else "TBD"}

EMERGENCY CONTACT
-----------------
{info.emergency_contact if info else "TBD"}

Have a safe journey!
""",
        recipients=[booking.email],
    )