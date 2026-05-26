from datetime import timezone

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from trekking_and_tour_management_system.guide_applications.models import GuideApplication

from trekking_and_tour_management_system.guide_applications.models import GuideApplication

from trekking_and_tour_management_system.guide_applications.services.guide_application_service import (
        create_guide_account,
        send_status_email,
        send_application_received_email,
    )
from trekking_and_tour_management_system.guides.models import Guide

@receiver(pre_save, sender=GuideApplication)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        instance._old_status = GuideApplication.objects.get(pk=instance.pk).status
    else:
        instance._old_status = None


@receiver(post_save, sender=GuideApplication)
def handle_status_change(sender, instance, created, **kwargs):

    # NEW APPLICATION CREATED
    if created:
        send_application_received_email(instance)
        return

    old_status = getattr(instance, "_old_status", None)

    if old_status == instance.status:
        return

    send_status_email(instance)

    if instance.status == "ACCEPTED":
        create_guide_account(instance)

@receiver(post_delete, sender=Guide)
def delete_related_user(sender, instance, **kwargs):
        
    if instance.user:
        instance.user.delete()

    if instance.created_from_application:
        application = instance.created_from_application
        application.account_deleted = True
        application.deleted_at = timezone.now()
        application.save()