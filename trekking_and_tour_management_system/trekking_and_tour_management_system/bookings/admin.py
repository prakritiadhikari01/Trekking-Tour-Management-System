from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "package",
        "booking_status",
        "payment_status",
        "assigned_guide",
        "created_at",
    ]

    list_filter = [
        "booking_status",
        "payment_status",
    ]

    search_fields = [
        "full_name",
        "email",
        "package__title",
    ]