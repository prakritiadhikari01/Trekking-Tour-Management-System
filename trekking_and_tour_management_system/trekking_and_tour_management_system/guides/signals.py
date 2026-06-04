from django.db.models.signals import post_save
from django.dispatch import receiver

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