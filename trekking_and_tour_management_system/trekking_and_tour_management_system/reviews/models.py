from django.db import models
from django.conf import settings

from trekking_and_tour_management_system.core.models import BaseModel

class Review(BaseModel):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="reviews")

    booking = models.OneToOneField("bookings.Booking",on_delete=models.CASCADE,related_name="review",null=True,  blank=True)

    package = models.ForeignKey("packages.TrekPackage",on_delete=models.CASCADE,related_name="reviews")

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.package} ({self.rating})"