#trekking_and_tour_management_system/core/models/base.py
from django.db import models
from core.utils.slug import generate_unique_slug

class TimeStampedModel(models.Model):
    """
    Abstract model providing created_at and updated_at fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(
        unique=True,
        blank=True
    )

    class Meta:
        abstract = True

    def get_slug_source(self):
        raise NotImplementedError(
            "Subclasses must implement get_slug_source()"
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(
                self.__class__,
                self.get_slug_source()
            )

        super().save(*args, **kwargs)
