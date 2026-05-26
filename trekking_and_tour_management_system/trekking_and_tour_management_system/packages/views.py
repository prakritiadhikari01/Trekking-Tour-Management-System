from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets

from trekking_and_tour_management_system.packages.api.serializers import TrekPackageSerializer

from .models import TrekPackage

def package_list(request):

    query = request.GET.get("q")

    packages = TrekPackage.objects.filter(available=True)

    if query:
        packages = packages.filter(
            Q(title__icontains=query)
            | Q(destination__icontains=query)
        )

    context = {
        "packages": packages,
    }

    return render(
        request,
        "packages/package_list.html",
        context,
    )

def package_detail(request, slug):

    package = get_object_or_404(
        TrekPackage,
        slug=slug,
        available=True,
    )

    context = {
        "package": package,
    }

    return render(
        request,
        "packages/package_detail.html",
        context,
    )
