#trekking_and_tour_management_system/packages/services/package_service.py
from decimal import Decimal

from django.core.exceptions import ValidationError

from trekking_and_tour_management_system.packages.models import (
    TrekPackage,
)


class PackageService:

    @staticmethod
    def create_package(data):

        if data["price"] <= 0:
            raise ValidationError(
                "Package price must be greater than 0."
            )

        if data["guide_price"] < 0:
            raise ValidationError(
                "Guide price cannot be negative."
            )

        return TrekPackage.objects.create(
            **data
        )

    @staticmethod
    def update_package(package, data):

        for field, value in data.items():
            setattr(package, field, value)

        package.save()

        return package

    @staticmethod
    def calculate_total_price(
        package,
        need_guide=False,
    ):

        total = Decimal(package.price)

        if need_guide:
            total += Decimal(
                package.guide_price
            )

        return total