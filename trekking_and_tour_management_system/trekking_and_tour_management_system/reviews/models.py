from django.db import models
from django.conf import settings


class Review(models.Model):
   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.CASCADE,
        related_name="review",
        null=True,   # TEMPORARY
        blank=True
    )

    package = models.ForeignKey(
        "packages.TrekPackage",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #unique_together = ("user", "package")  # one review per user per package
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.package} ({self.rating})"