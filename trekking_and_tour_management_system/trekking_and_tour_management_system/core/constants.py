# trekking_and_tour_management_system/core/constants.py

from django.db import models

# BOOKING RELATED CHOICES

class BookingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"

class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"

class RefundStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    REJECTED = "REJECTED", "Rejected"

# GUIDE RELATED CHOICES

class GuideStatus(models.TextChoices):
    NOT_ASSIGNED = "NOT_ASSIGNED", "Not Assigned"
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    EXPIRED = "EXPIRED", "Expired"


class GuideApplicationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"


# TREK / PACKAGE RELATED
class DifficultyLevel(models.TextChoices):
    EASY = "EASY", "Easy"
    MODERATE = "MODERATE", "Moderate"
    HARD = "HARD", "Hard"