from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from trekking_and_tour_management_system.packages.models import TrekPackage
from trekking_and_tour_management_system.packages.api.v1.serializers import (
    TrekPackageSerializer,
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

class TrekPackageViewSet(viewsets.ModelViewSet):

    serializer_class = TrekPackageSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get_queryset(self):

        user = self.request.user
        query = self.request.query_params.get("q")

        is_admin = (
            user.is_authenticated
            and user.role == "admin"
        )

        if is_admin:

            queryset = (
                search_all_packages(query)
                if query
                else get_all_packages()
            )

        else:

            queryset = (
                search_available_packages(query)
                if query
                else get_available_packages()
            )

        return queryset

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