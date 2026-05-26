from django.db import models
from django.conf import settings
from trekking_and_tour_management_system.packages.models import TrekPackage


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(TrekPackage, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.package.title}"
