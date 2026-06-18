# guides/models.py
from django.db import models
from django.conf import settings

from core.models import TimeStampedModel
from trekking_and_tour_management_system.core.validators import validate_phone_number


class Guide(TimeStampedModel):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guide_profile")

    full_name = models.CharField(max_length=255)

    phone_number = models.CharField(
        max_length=20,
        validators=[
            validate_phone_number
        ]
    )
    experience = models.TextField()

    languages = models.CharField(max_length=255)

    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name