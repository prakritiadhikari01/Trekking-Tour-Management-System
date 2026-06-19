# bookings/models.py
from django.conf import settings
from django.db import models
from core.models import TimeStampedModel

from trekking_and_tour_management_system.core.constants import BookingStatus, GuideStatus
from trekking_and_tour_management_system.core.validators import validate_phone_number



    
class Booking(TimeStampedModel):

    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey("packages.TrekPackage", on_delete=models.CASCADE, related_name="bookings")
    need_guide = models.BooleanField( default=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    need_guide = models.BooleanField(
        default=False
    )
    guide_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    assigned_guide = models.ForeignKey(
        "guides.Guide",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_bookings"
    )
    guide_status = models.CharField(
        max_length=20,
        choices=GuideStatus.choices,
        default=GuideStatus.NOT_ASSIGNED,
    )
    guide_assigned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    assigned_guide = models.ForeignKey( "guides.Guide",  on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_bookings")

    guide_status = models.CharField( max_length=20, choices=GuideStatus.choices,  default=GuideStatus.NOT_ASSIGNED)

    guide_assigned_at = models.DateTimeField( null=True,  blank=True)

    guide_responded_at = models.DateTimeField( null=True,blank=True)

    guide_response_deadline = models.DateTimeField( null=True, blank=True, )

    full_name = models.CharField(max_length=255)

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
        validators=[
            validate_phone_number
        ]
    )

    number_of_people = models.PositiveIntegerField(default=1)

    trip_start_date = models.DateField()

    trip_end_date = models.DateField(null=True, blank=True)

    special_request = models.TextField(  blank=True,  null=True)

    total_price = models.DecimalField(  max_digits=10, decimal_places=2,  default=0)

    booking_status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    khalti_pidx = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    cancellation_reason = models.TextField(null=True, blank=True)
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.package.title}"