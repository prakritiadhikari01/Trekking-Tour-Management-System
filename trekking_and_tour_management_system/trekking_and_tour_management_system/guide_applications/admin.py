from django.contrib import admin

from .models import GuideApplication


@admin.register(GuideApplication)
class GuideApplicationAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "created_at",
    ]

    search_fields = [
        "user__email",
        "user__name",
        "portfolio_link",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]