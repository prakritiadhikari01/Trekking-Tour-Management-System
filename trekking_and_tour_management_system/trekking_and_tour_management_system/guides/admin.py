from django.contrib import admin

from trekking_and_tour_management_system.guides.models import Guide
from trekking_and_tour_management_system.guides.services.guide_services import create_guide_by_admin



@admin.register(Guide)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone_number",
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