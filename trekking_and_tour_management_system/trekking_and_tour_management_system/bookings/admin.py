# bookings/admin.py
from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "package",
        "assigned_guide",
        "guide_status",
        "booking_status",
        "trip_start_date",
        "total_price",
        "created_at",
    )

    list_filter = (
        "booking_status",
        "guide_status",
        "trip_start_date",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone_number",
        "package__title",
        "assigned_guide__full_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "guide_assigned_at",
        "guide_responded_at",
    )

    fieldsets = (
        (
            "Booking Information",
            {
                "fields": (
                    "user",
                    "package",
                    "booking_status",
                    "total_price",
                    "number_of_people",
                    "need_guide",

                )
            },
        ),

        (
            "Customer Information",
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone_number",
                )
            },
        ),

        (
            "Trip Information",
            {
                "fields": (
                    "trip_start_date",
                    "trip_end_date",
                    "special_request",
                )
            },
        ),

        (
            "Guide Information",
            {
                "fields": (
                    "guide_price",
                    "assigned_guide",
                    "guide_status",
                    "guide_assigned_at",
                    "guide_responded_at",
                )
            },
        ),

        (
            "Cancellation Information",
            {
                "fields": (
                    "cancellation_reason",
                    "cancelled_at",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )