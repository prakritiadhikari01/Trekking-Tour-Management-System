# bookings/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from trekking_and_tour_management_system.bookings.services.customer_email_service import send_customer_accept_email
from trekking_and_tour_management_system.bookings.services.guide_email_service import send_guide_assignment_email

from .models import Booking


@receiver(pre_save, sender=Booking)
def store_old_booking_state(sender, instance, **kwargs):

    if instance.pk:
        old = Booking.objects.get(pk=instance.pk)
        instance._old_guide = old.assigned_guide
        instance._old_status = old.guide_status
    else:
        instance._old_guide = None
        instance._old_status = None


@receiver(post_save, sender=Booking)
def handle_booking_changes(sender, instance, created, **kwargs):

    # GUIDE ASSIGNMENT EMAIL
    if instance.assigned_guide and instance._old_guide != instance.assigned_guide:
        instance.guide_assigned_at = timezone.now()
        instance.save(update_fields=["guide_assigned_at"])

        send_guide_assignment_email(instance)

    # GUIDE ACCEPT / REJECT CUSTOMER EMAIL
    if instance._old_status != instance.guide_status:

        instance.guide_responded_at = timezone.now()
        instance.save(update_fields=["guide_responded_at"])

        if instance.guide_status == "ACCEPTED":
            send_customer_accept_email(instance)