#trekking_and_tour_management_system/packages/admin.py
from django.contrib import admin

from .models import Category, TrekPackageInfo
from .models import TrekPackage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TrekPackage)
class TrekPackageAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "category",
        "destination",
        "price",
        "guide_price",
        "difficulty",
        "featured",
        "available",
    ]

    list_filter = [
        "difficulty",
        "featured",
        "available",
           "category",
    ]

    search_fields = [
        "title",
        "destination",
    ]

    prepopulated_fields = {
        "slug": ("title",)
    }
    

@admin.register(TrekPackageInfo)
class TrekPackageInfoAdmin(admin.ModelAdmin):
    list_display = (
        "package",
        "meeting_point",
        "emergency_contact",
    )