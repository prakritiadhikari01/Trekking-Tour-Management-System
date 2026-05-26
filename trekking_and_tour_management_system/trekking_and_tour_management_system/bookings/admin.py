from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "package",
        "full_name",
        "email",
        "phone_number",
        "number_of_people",
        "travel_date",
        "booking_status",
        "total_price",
        "created_at",
    )

    list_filter = (
        "booking_status",
        "travel_date",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone_number",
        "package__title",
    )
