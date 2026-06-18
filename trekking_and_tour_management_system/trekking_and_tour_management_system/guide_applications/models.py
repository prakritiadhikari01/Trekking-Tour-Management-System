from django.db import models

from trekking_and_tour_management_system.core.models import BaseModel
from trekking_and_tour_management_system.core.choices import GuideApplicationStatus

class GuideApplication(BaseModel):
    
    full_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=20)

    experience = models.TextField()

    languages = models.CharField(max_length=255)

    cv = models.FileField(upload_to="guide_applications/cv/")

    citizenship_document = models.FileField(upload_to="guide_applications/documents/", null=True, blank=True)

    status = models.CharField(max_length=20, choices=GuideApplicationStatus.choices, default=GuideApplicationStatus.PENDING)

    
    account_deleted = models.BooleanField(default=False)

   
    def __str__(self):
        return self.full_name