from django.contrib import admin
from django.core.exceptions import ValidationError

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.guides.models import Guide
from trekking_and_tour_management_system.guides.selectors.guide_availability_selectors import get_available_guides_for_booking
from trekking_and_tour_management_system.guides.services.guide_assignment_service import (
    GuideAssignmentService,
)


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

    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs,
    ):
        """
        Show only available guides when editing a booking.
        Uses the same availability logic as the API.
        """

        if db_field.name == "assigned_guide":

            booking_id = request.resolver_match.kwargs.get(
                "object_id"
            )

            if booking_id:

                try:
                    kwargs["queryset"] = (
                        get_available_guides_for_booking(
                            booking_id=int(booking_id)
                        )
                    )

                except Exception:
                    kwargs["queryset"] = Guide.objects.none()

            else:
                kwargs["queryset"] = Guide.objects.none()

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):
        """
        Route guide assignment through
        GuideAssignmentService so admin
        uses the exact same business rules
        as the API.
        """

        if change:

            old_obj = Booking.objects.get(
                pk=obj.pk
            )

            old_guide = old_obj.assigned_guide
            new_guide = obj.assigned_guide

            if (
                new_guide
                and old_guide != new_guide
            ):

                try:

                    GuideAssignmentService.assign_guide(
                        booking_id=obj.id,
                        guide_id=new_guide.id,
                    )

                    return

                except ValueError as e:

                    raise ValidationError(
                        str(e)
                    )

        super().save_model(
            request,
            obj,
            form,
            change,
        )