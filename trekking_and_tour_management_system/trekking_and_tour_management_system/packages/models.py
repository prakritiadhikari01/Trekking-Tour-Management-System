from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from core.models import (
    TimeStampedModel,
    SlugModel,
)
from trekking_and_tour_management_system.core.constants import DifficultyLevel



class Category(SlugModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return self.name
    
    
    



class TrekPackage(TimeStampedModel, SlugModel):

    title = models.CharField(max_length=255)

    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="packages")

    destination = models.CharField(max_length=255)

    duration = models.PositiveIntegerField(help_text="Duration in days")

    price = models.DecimalField(max_digits=10, decimal_places=2)

    guide_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    difficulty = models.CharField(max_length=20, choices=DifficultyLevel.choices, default=DifficultyLevel.EASY)

    description = models.TextField()

    image = models.ImageField(upload_to="trek_packages/")

    featured = models.BooleanField(default=False)

    available = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
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
    package = models.OneToOneField("packages.TrekPackage",on_delete=models.CASCADE,related_name="info")

    meeting_point = models.TextField()

    required_items = models.TextField()

    emergency_contact = models.CharField(max_length=100)

    guide_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.package.title