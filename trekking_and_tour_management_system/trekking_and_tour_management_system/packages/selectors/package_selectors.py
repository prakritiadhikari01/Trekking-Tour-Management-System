from django.db.models import Q

from trekking_and_tour_management_system.packages.models import (
    TrekPackage,
)


def get_available_packages():
    return TrekPackage.objects.filter(
        available=True
    )


def get_all_packages():
    return TrekPackage.objects.all()


def get_package_by_id(package_id):
    return TrekPackage.objects.get(
        id=package_id
    )


def get_package_by_slug(slug):
    return TrekPackage.objects.get(
        slug=slug
    )


def get_featured_packages():
    return TrekPackage.objects.filter(
        featured=True,
        available=True,
    )


def search_available_packages(query):
    return TrekPackage.objects.filter(
        Q(title__icontains=query)
        | Q(destination__icontains=query),
        available=True,
    )


def search_all_packages(query):
    return TrekPackage.objects.filter(
        Q(title__icontains=query)
        | Q(destination__icontains=query)
    )