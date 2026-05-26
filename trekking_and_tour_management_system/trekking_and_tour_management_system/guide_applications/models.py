from django.db import models

class GuideApplication(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    experience = models.TextField()
    languages = models.CharField(max_length=255)

    cv = models.FileField(upload_to="guide_applications/cv/")
    citizenship_document = models.FileField(upload_to="guide_applications/documents/", null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    account_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.full_name