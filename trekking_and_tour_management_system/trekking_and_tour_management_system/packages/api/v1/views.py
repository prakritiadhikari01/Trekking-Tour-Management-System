#trekking_and_tour_management_system/packages/api/v1/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from trekking_and_tour_management_system.packages.api.v1.serializers import TrekPackageReadSerializer, TrekPackageWriteSerializer
from trekking_and_tour_management_system.packages.models import TrekPackage
from trekking_and_tour_management_system.packages.services.package_query_service import (
    PackageQueryService,
)

from trekking_and_tour_management_system.packages.selectors.package_selectors import (
    get_available_packages,
    search_all_packages,
    search_available_packages,
    get_all_packages,
)

from trekking_and_tour_management_system.core.permissions import (
    IsAdmin,
)

from rest_framework.permissions import SAFE_METHODS
from rest_framework.parsers import MultiPartParser, FormParser

from trekking_and_tour_management_system.packages.services.package_service import PackageService

class TrekPackageViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            return TrekPackageReadSerializer

        return TrekPackageWriteSerializer
    
    parser_classes = [MultiPartParser, FormParser]
    def get_queryset(self):

        return (
            PackageQueryService.get_packages(
                user=self.request.user,
                query=self.request.query_params.get("q"),
            )
        )
    
    def perform_create(
        self,
        serializer,
    ):
        PackageService.create_package(
            serializer.validated_data
        )
    def perform_update(
        self,
        serializer,
    ):
        PackageService.update_package(
            self.get_object(),
            serializer.validated_data,
        )

    
    def get_permissions(self):

        if self.request.method in SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]

        return [IsAdmin()]
    
    def destroy(self, request, *args, **kwargs):
        package = self.get_object()

        self.perform_destroy(package)

        return Response(
            {
                "message": "Package deleted successfully."
            },
            status=status.HTTP_200_OK,
        )