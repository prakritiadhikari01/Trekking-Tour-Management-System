# trekking_and_tour_management_system/core/models/base.py

from django.db import models
from django.utils.text import slugify
from core.utils.slug import generate_unique_slug


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides:
    - created_at
    - updated_at
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Abstract base model that auto-generates unique slugs.
    Requires child model to define get_slug_source().
    """

    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def get_slug_source(self):
        """
        Must be implemented by child models.
        Example: return self.name
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_slug_source()"
        )

    def save(self, *args, **kwargs):
        """
        Auto-generate slug if not provided.
        """
        if not self.slug:
            source = self.get_slug_source()

            # fallback safety (optional but good practice)
            if not source:
                raise ValueError("Slug source cannot be empty")

            self.slug = generate_unique_slug(
                self.__class__,
                source
            )

        super().save(*args, **kwargs)