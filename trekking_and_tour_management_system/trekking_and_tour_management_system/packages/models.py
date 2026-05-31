from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class TrekPackage(models.Model):

    DIFFICULTY_CHOICES = (
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("hard", "Hard"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    destination = models.CharField(max_length=255)

    duration = models.PositiveIntegerField(
        help_text="Duration in days"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="easy"
    )
    description = models.TextField()

    image = models.ImageField(
        upload_to="trek_packages/"
    )

    featured = models.BooleanField(default=False)

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "packages:package_detail",
            kwargs={"slug": self.slug}
        )

    def __str__(self):
        return self.title
    
class TrekPackageInfo(models.Model):
    package = models.OneToOneField(
        "packages.TrekPackage",
        on_delete=models.CASCADE,
        related_name="info"
    )

    meeting_point = models.TextField()
    required_items = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    guide_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.package.title