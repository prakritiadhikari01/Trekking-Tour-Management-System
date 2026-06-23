from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.payments.models import Payment
from trekking_and_tour_management_system.core.tasks import (
    generate_invoice_task,
    send_payment_failed_email_task,
    send_payment_success_email_task,
)


@receiver(pre_save, sender=Payment)
def cache_previous_payment_status(sender, instance: Payment, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return
    old = Payment.objects.filter(pk=instance.pk).values("status").first()
    instance._previous_status = old["status"] if old else None


@receiver(post_save, sender=Payment)
def payment_status_changed(sender, instance: Payment, created: bool, **kwargs):
    if created:
        return
    previous = getattr(instance, "_previous_status", None)
    if previous == instance.status:
        return

    if instance.status == "COMPLETED":
        Booking.objects.filter(id=instance.booking_id).exclude(booking_status="CONFIRMED").update(
            booking_status="CONFIRMED",
        )
        generate_invoice_task.delay(instance.id)
        send_payment_success_email_task.delay(instance.id)
    elif instance.status == "FAILED":
        send_payment_failed_email_task.delay(instance.id)
