from django.contrib import admin

from .models import Category
from .models import TrekPackage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TrekPackage)
class TrekPackageAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "destination",
        "price",
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
