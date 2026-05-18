from django.db import models

class TrekPackage(models.Model):
    title = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title