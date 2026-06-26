from trekking_and_tour_management_system.packages.models import (
    TrekPackage,
)


class PackageRepository:

    @staticmethod
    def get_queryset():
        return (
            TrekPackage.objects
            .select_related("category")
        )

    @staticmethod
    def create(**data):
        return TrekPackage.objects.create(
            **data
        )

    @staticmethod
    def update(package, **data):

        for field, value in data.items():
            setattr(package, field, value)

        package.save()

        return package