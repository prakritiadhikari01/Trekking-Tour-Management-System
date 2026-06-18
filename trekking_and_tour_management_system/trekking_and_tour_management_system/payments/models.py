from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from core.constants.choices import PaymentStatus, RefundStatus
from core.models.base import TimeStampedModel

class Payment(TimeStampedModel):
    
    booking = models.OneToOneField("bookings.Booking",on_delete=models.CASCADE,related_name="payment")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    pidx = models.CharField(max_length=255, null=True, blank=True)  

    payment_url = models.URLField(max_length=500, null=True, blank=True)

    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)


    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"


class Invoice(TimeStampedModel):
    payment = models.OneToOneField(
        "payments.Payment",
        on_delete=models.CASCADE,
        related_name="invoice",
    )
    booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.CASCADE,
        related_name="invoice",
    )
    invoice_id = models.CharField(max_length=32, unique=True)
    access_token = models.CharField(max_length=64, unique=True)
    file = models.FileField(upload_to="invoices/%Y/%m/")

    booking = models.OneToOneField("bookings.Booking",on_delete=models.CASCADE,related_name="invoice",)

    invoice_id = models.CharField(max_length=32, unique=True)

    access_token = models.CharField(max_length=64, unique=True)

    file = models.FileField(upload_to="invoices/%Y/%m/")
   
    @staticmethod
    def build_invoice_id(payment_id: int) -> str:
        return f"INV-{timezone.now():%Y%m%d}-{payment_id:06d}"

    @staticmethod
    def build_access_token() -> str:
        return get_random_string(48)

    def __str__(self):
        return self.invoice_id

class NotificationDispatch(models.Model):
    unique_key = models.CharField(max_length=128, unique=True)

    event_type = models.CharField(max_length=64)
    booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_dispatches",
    )
    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_dispatches",
    )

    def __str__(self):
        return self.unique_key

class Refund(TimeStampedModel):

    booking = models.OneToOneField("bookings.Booking",on_delete=models.CASCADE,related_name="refund")

    refund_percentage = models.PositiveIntegerField()

    refund_amount = models.DecimalField(max_digits=10,decimal_places=2)

    payment_method = models.CharField(max_length=50,blank=True)

    refund_account = models.CharField(max_length=255,blank=True)

    admin_note = models.TextField(blank=True)

    status = models.CharField(max_length=20,choices=RefundStatus.choices,default=RefundStatus.PENDING)

    completed_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Refund #{self.id}"