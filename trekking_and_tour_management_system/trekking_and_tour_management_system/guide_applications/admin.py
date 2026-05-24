from django.contrib import admin
from .models import GuideApplication


@admin.register(GuideApplication)
class GuideApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "status")