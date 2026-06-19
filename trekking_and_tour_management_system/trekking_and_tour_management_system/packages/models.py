#trekking_and_tour_management_system/packages/models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

from core.models import TimeStampedModel, SlugModel
from core.constants import DifficultyLevel


class Category(SlugModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
        ]

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return self.name


class TrekPackage(TimeStampedModel, SlugModel):

    title = models.CharField(max_length=255)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="packages",
        db_index=True
    )

    destination = models.CharField(max_length=255, db_index=True)

    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration in days"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    guide_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.EASY,
        db_index=True
    )

    description = models.TextField()

    image = models.ImageField(upload_to="packages/images/")

    featured = models.BooleanField(default=False, db_index=True)

    available = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["available"]),
            models.Index(fields=["featured"]),
        ]

    def get_slug_source(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "packages:package_detail",
            kwargs={"slug": self.slug}
        )

    def __str__(self):
        return self.title


class TrekPackageInfo(TimeStampedModel):
    package = models.OneToOneField(
        "packages.TrekPackage",
        on_delete=models.CASCADE,
        related_name="info"
    )

    meeting_point = models.TextField()
    required_items = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    guide_notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["emergency_contact"]
            )
        ]
    def __str__(self):
        return self.package.title