from django.db import models
from django.conf import settings


class Guide(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    experience = models.TextField()
    languages = models.CharField(max_length=255)

    created_from_application = models.OneToOneField(
        "guide_applications.GuideApplication",
        on_delete=models.CASCADE
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.full_name