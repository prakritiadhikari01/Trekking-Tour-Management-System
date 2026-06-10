from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.guides.models import Guide
from trekking_and_tour_management_system.guides.tasks import (
    send_guide_creation_email_task,
)


@receiver(post_save, sender=Guide)
def send_guide_creation_email(
    sender,
    instance,
    created,
    **kwargs,
):
    if not created:
        return

    send_guide_creation_email_task.delay(
        instance.user.id
    )

@receiver(pre_save, sender=Booking)
def cache_previous_guide(sender, instance, **kwargs):

    if not instance.pk:
        instance._previous_guide_id = None
        return

    old = Booking.objects.filter(
        pk=instance.pk
    ).values(
        "assigned_guide_id"
    ).first()

    instance._previous_guide_id = (
        old["assigned_guide_id"]
        if old else None
    )

@receiver(pre_save, sender=Booking)
def cache_previous_assigned_guide(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_assigned_guide = None
        return

    old = Booking.objects.filter(pk=instance.pk).values("assigned_guide_id").first()
    instance._previous_assigned_guide = old["assigned_guide_id"] if old else None