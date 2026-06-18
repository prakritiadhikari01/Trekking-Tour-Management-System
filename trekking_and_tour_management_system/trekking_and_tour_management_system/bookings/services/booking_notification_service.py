from core.services.email_service import EmailService


class BookingNotificationService:

    @staticmethod
    def notify_guide_assignment(booking):
        guide = booking.assigned_guide
        info = booking.package.info

        message = f"""
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
"""

        EmailService.send_plain_email(
            subject="New Trek Assignment",
            message=message,
            recipient_list=[guide.user.email],
        )

    @staticmethod
    def notify_customer_accepted(booking):
        guide = booking.assigned_guide
        info = booking.package.info

        message = f"""
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
"""

        EmailService.send_plain_email(
            subject="Your Trek Has Been Confirmed",
            message=message,
            recipient_list=[booking.email],
        )

    @staticmethod
    def notify_admin_guide_response(booking):
        message = f"""
Hello Admin,

The guide {booking.assigned_guide.full_name}
has responded to booking #{booking.id}.

Guide Status:
{booking.guide_status}

Booking Status:
{booking.booking_status}

Please review the booking.
"""

        EmailService.send_plain_email(
            subject="Guide Responded to Assignment",
            message=message,
            recipient_list=["admin@example.com"],  # Replace later
        )