import requests
from django.conf import settings

from trekking_and_tour_management_system.payments.models import Payment


def ensure_khalti_payment_link(payment: Payment) -> Payment:
    if payment.status != "PENDING":
        return payment
    if payment.pidx and payment.payment_url:
        return payment

    base_url = getattr(settings, "APP_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    payload = {
        "return_url": f"{base_url}/api/payments/verify/",
        "website_url": base_url,
        "amount": int(payment.amount * 100),
        "purchase_order_id": str(payment.id),
        "purchase_order_name": f"Booking #{payment.booking_id}",
    }
    response = requests.post(
        settings.KHALTI_INITIATE_URL,
        json=payload,
        headers={
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("pidx") or not data.get("payment_url"):
        raise ValueError("Invalid Khalti initiate response")

    Payment.objects.filter(id=payment.id, status="PENDING").update(
        pidx=data["pidx"],
        payment_url=data["payment_url"],
    )
    payment.refresh_from_db(fields=["pidx", "payment_url"])
    return payment
