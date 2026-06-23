from celery import shared_task
from django.conf import settings

from trekking_and_tour_management_system.payments.models import (
    NotificationDispatch,
    Payment,
)
from trekking_and_tour_management_system.core.services.email_services import (
    send_event_emails,
)
from trekking_and_tour_management_system.core.services.invoice_service import (
    generate_or_update_invoice,
)
from trekking_and_tour_management_system.core.services.khalti_service import (
    ensure_khalti_payment_link,
)


def _mark_once(unique_key: str, *, event_type: str, payment: Payment):
    return NotificationDispatch.objects.get_or_create(
        unique_key=unique_key,
        defaults={
            "event_type": event_type,
            "booking": payment.booking,
            "payment": payment,
        },
    )


def _common_context(payment: Payment, extra: dict | None = None) -> dict:
    booking = payment.booking
    package = booking.package
    base_url = getattr(settings, "APP_BASE_URL", "").rstrip("/")
    context = {
        "customer_name": booking.full_name,
        "booking_id": booking.id,
        "package_title": package.title,
        "trip_start_date": booking.trip_start_date,
        "trip_end_date": booking.trip_end_date,
        "number_of_people": booking.number_of_people,
        "total_price": booking.total_price,
        "booking_status": booking.booking_status,
        "payment_status": payment.status,
        "payment_reference": payment.transaction_id or payment.pidx or "N/A",
        "support_email": settings.DEFAULT_FROM_EMAIL,
        "payment_link": payment.payment_url or f"{base_url}/api/payments/initiate/",
        "dashboard_link": f"{base_url}/dashboard/bookings/",
    }
    if extra:
        context.update(extra)
    return context


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_booking_created_email_task(self, payment_id: int) -> None:
    payment = Payment.objects.select_related("booking", "booking__package").get(id=payment_id)
    payment = ensure_khalti_payment_link(payment)
    unique_key = f"booking_created:{payment.booking_id}"
    _, created = _mark_once(unique_key, event_type="booking_created", payment=payment)
    if not created:
        return
    context = _common_context(payment)
    send_event_emails(
        user_subject=f"Booking received #{payment.booking_id}",
        admin_subject=f"New booking pending #{payment.booking_id}",
        user_template="emails/booking_created_user.html",
        admin_template="emails/booking_created_admin.html",
        context=context,
        user_email=payment.booking.email,
    )


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_invoice_task(self, payment_id: int) -> int:
    invoice = generate_or_update_invoice(payment_id)
    return invoice.id


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_payment_success_email_task(self, payment_id: int) -> None:
    payment = Payment.objects.select_related("booking", "booking__package").get(id=payment_id)
    unique_key = f"payment_success:{payment.id}"
    _, created = _mark_once(unique_key, event_type="payment_success", payment=payment)
    if not created:
        return
    invoice = generate_or_update_invoice(payment.id)
    base_url = getattr(settings, "APP_BASE_URL", "").rstrip("/")
    context = _common_context(
        payment,
        {
            "invoice_id": invoice.invoice_id,
            "invoice_url": f"{base_url}/api/payments/invoices/{invoice.access_token}/download/",
        },
    )
    send_event_emails(
        user_subject=f"Payment successful - Booking #{payment.booking_id} confirmed",
        admin_subject=f"Booking confirmed #{payment.booking_id}",
        user_template="emails/payment_success_user.html",
        admin_template="emails/payment_success_admin.html",
        context=context,
        user_email=payment.booking.email,
    )


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_payment_failed_email_task(self, payment_id: int) -> None:
    payment = Payment.objects.select_related("booking", "booking__package").get(id=payment_id)
    unique_key = f"payment_failed:{payment.id}:{payment.status}"
    _, created = _mark_once(unique_key, event_type="payment_failed", payment=payment)
    if not created:
        return
    context = _common_context(payment)
    send_event_emails(
        user_subject=f"Payment failed - Booking #{payment.booking_id}",
        admin_subject=f"Payment failed alert #{payment.booking_id}",
        user_template="emails/payment_failed_user.html",
        admin_template="emails/payment_failed_admin.html",
        context=context,
        user_email=payment.booking.email,
    )


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_booking_cancelled_email_task(self, payment_id: int) -> None:
    payment = Payment.objects.select_related("booking", "booking__package").get(id=payment_id)
    unique_key = f"booking_cancelled:{payment.booking_id}"
    _, created = _mark_once(unique_key, event_type="booking_cancelled", payment=payment)
    if not created:
        return
    context = _common_context(payment)
    send_event_emails(
        user_subject=f"Booking cancelled #{payment.booking_id}",
        admin_subject=f"Booking cancelled alert #{payment.booking_id}",
        user_template="emails/booking_cancelled_user.html",
        admin_template="emails/booking_cancelled_admin.html",
        context=context,
        user_email=payment.booking.email,
    )
