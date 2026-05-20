from trekking_and_tour_management_system.packages.models import TrekPackage


class PackageService:

    @staticmethod
    def create_package(data):
        return TrekPackage.objects.create(**data)

    @staticmethod
    def update_package(package, data):
        for attr, value in data.items():
            setattr(package, attr, value)

        package.save()

        return package