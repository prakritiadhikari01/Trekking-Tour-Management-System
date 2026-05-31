from django.db import models
from django.conf import settings


class Review(models.Model):
    """
    Review model for Trek Packages
    """

    # user who wrote the review
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    # IMPORTANT: use string reference (prevents import crash)
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
        unique_together = ("user", "package")  # one review per user per package
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.package} ({self.rating})"