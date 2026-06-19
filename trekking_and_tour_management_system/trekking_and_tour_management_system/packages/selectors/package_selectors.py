from django.db.models import Q

from trekking_and_tour_management_system.packages.repositories.package_repository import (
    PackageRepository,
)


def get_available_packages():

    return (
        PackageRepository.get_queryset()
        .filter(available=True)
    )


def get_all_packages():

    return (
        PackageRepository.get_queryset()
    )


def get_package_by_id(package_id):

    return (
        PackageRepository.get_queryset()
        .get(id=package_id)
    )


def get_package_by_slug(slug):

    return (
        PackageRepository.get_queryset()
        .get(slug=slug)
    )


def get_featured_packages():

    return (
        PackageRepository.get_queryset()
        .filter(
            featured=True,
            available=True,
        )
    )


def search_available_packages(query):

    return (
        PackageRepository.get_queryset()
        .filter(
            Q(title__icontains=query)
            | Q(destination__icontains=query),
            available=True,
        )
    )


def search_all_packages(query):

    return (
        PackageRepository.get_queryset()
        .filter(
            Q(title__icontains=query)
            | Q(destination__icontains=query)
        )
    )