from django.db.models import Q

from trekking_and_tour_management_system.packages.models import TrekPackage


def get_available_packages():
    return TrekPackage.objects.filter(available=True)


def search_packages(query):
    return TrekPackage.objects.filter(
        Q(title__icontains=query)
        | Q(destination__icontains=query),
        available=True,
    )


def get_all_packages():
    return TrekPackage.objects.all()