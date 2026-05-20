# payments/models.py

from django.conf import settings
from django.db import models


class Payment(models.Model):

    booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=50, default="khalti")

    transaction_id = models.CharField(max_length=200, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ),
        default="pending"
    )

    khalti_pidx = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking} - {self.status}"