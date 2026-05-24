from django.contrib import admin

from trekking_and_tour_management_system.guides.models import Guide



@admin.register(Guide)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone_number",
        "address",
        "experience",
        "languages",
        "is_verified",
        "created_at",
    ]

    search_fields = [
        "user__email",
        "phone_number",
    ]

    list_filter = [
        "is_verified",
    ]   