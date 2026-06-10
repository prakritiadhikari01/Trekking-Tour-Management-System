from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from trekking_and_tour_management_system.bookings.models import Booking

from trekking_and_tour_management_system.guides.services.admin_email_service import send_admin_notification_email
from trekking_and_tour_management_system.guides.services.customer_email_service import (
    send_customer_accept_email,
)

from trekking_and_tour_management_system.guides.services.guide_email_service import (
    
    send_guide_account_ready_email,
)
from trekking_and_tour_management_system.guides.services.guide_assignment_expiry_service import (
    GuideAssignmentExpiryService,
)

User = get_user_model()

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


@shared_task
def send_guide_creation_email_task(user_id):
    user = User.objects.get(id=user_id)

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = PasswordResetTokenGenerator().make_token(
        user
    )

    reset_link = (
        f"{settings.APP_BASE_URL}"
        f"/api/auth/password-reset-confirm/"
        f"{uid}/{token}/"
    )

    send_guide_account_ready_email(
        user,
        reset_link,
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


@shared_task
def expire_pending_guide_assignments():
    return (
        GuideAssignmentExpiryService.expire_pending_assignments()
    )

@shared_task
def test_task():
    print("CELERY WORKS")


