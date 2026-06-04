# bookings/guide_assignment_service.py

from django.utils import timezone



def assign_guide_to_booking(booking, guide):

    booking.assigned_guide = guide
    booking.guide_status = "PENDING"
    booking.guide_assigned_at = timezone.now()

    booking.save()

