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
        "trip_start_date",
        "trip_end_date",
        "booking_status",
        "total_price",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "booking_status",
        "trip_start_date",
        "trip_end_date",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone_number",
        "package__title",
    )
