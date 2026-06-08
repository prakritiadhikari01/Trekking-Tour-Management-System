from django.contrib import admin

from trekking_and_tour_management_system.guides.models import Guide


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "full_name",
        "user",
        "phone_number",
        "languages",
        "is_verified",
        "created_at",
    ]

    search_fields = [
        "full_name",
        "user__email",
        "phone_number",
    ]

    list_filter = [
        "is_verified",
        "created_at",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]