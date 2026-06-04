from celery import shared_task

from trekking_and_tour_management_system.bookings.models import Booking

from trekking_and_tour_management_system.bookings.services.customer_email_service import (
    send_customer_accept_email,
)

from trekking_and_tour_management_system.bookings.services.guide_email_service import (
    send_admin_notification_email,
)


@shared_task
def send_customer_accept_email_task(
    booking_id,
):
    print(f"Celery Sending customer accept email for booking id: {booking_id}")
    booking = Booking.objects.get(
        id=booking_id
    )

    send_customer_accept_email(
        booking
    )
    print(f"CELERY TASK FINISHED (Customer Got The TREK/TOUR info): {booking_id}")

@shared_task
def send_admin_notification_email_task(
    booking_id,
):
    print(f"Celery Sending admin notification email for booking id: {booking_id}")
    booking = Booking.objects.get(
        id=booking_id
    )

    send_admin_notification_email(
        booking
    )

    print(f"CELERY TASK FINISHED (Admin Got The Guide Acceptance/Rejection info): {booking_id}")