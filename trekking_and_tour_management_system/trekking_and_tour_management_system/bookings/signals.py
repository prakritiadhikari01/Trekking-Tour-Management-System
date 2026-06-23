from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.guides.services.guide_email_service import send_guide_assignment_email
from trekking_and_tour_management_system.payments.models import Payment
from trekking_and_tour_management_system.core.tasks import (
    send_booking_cancelled_email_task,
    send_booking_created_email_task,
)


@receiver(pre_save, sender=Booking)
def cache_previous_booking_status(sender, instance: Booking, **kwargs):
    if not instance.pk:
        instance._previous_booking_status = None
        return
    old = Booking.objects.filter(pk=instance.pk).values("booking_status").first()
    instance._previous_booking_status = old["booking_status"] if old else None


@receiver(post_save, sender=Booking)
def booking_events(sender, instance: Booking, created: bool, **kwargs):
    
    if created:
        payment = Payment.objects.filter(booking=instance).first()
        if payment is None:
            payment = Payment.objects.create(
                booking=instance,
                user=instance.user,
                amount=instance.total_price,
                status="PENDING",
            )
        send_booking_created_email_task.delay(payment.id)
        return

    previous = getattr(instance, "_previous_booking_status", None)
    if previous != "CANCELLED" and instance.booking_status == "CANCELLED":
        payment = Payment.objects.filter(booking=instance).first()
        if payment is None:
            payment = Payment.objects.create(
                booking=instance,
                user=instance.user,
                amount=instance.total_price,
                status="FAILED",
            )
        send_booking_cancelled_email_task.delay(payment.id)
    
    previous_guide = getattr(instance, "_previous_guide_id", None)
    if instance.assigned_guide and previous_guide != instance.assigned_guide_id:
        send_guide_assignment_email(instance)
