from django.db import models
from core.utils.slug import generate_unique_slug


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Auto slug generator with guaranteed uniqueness.
    """

    slug = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        abstract = True

    def get_slug_source(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_slug_source()"
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            source = self.get_slug_source()

            if not source:
                raise ValueError("Slug source cannot be empty")

            self.slug = generate_unique_slug(
                model=self.__class__,
                value=source,
                slug_field="slug"
            )

        super().save(*args, **kwargs)