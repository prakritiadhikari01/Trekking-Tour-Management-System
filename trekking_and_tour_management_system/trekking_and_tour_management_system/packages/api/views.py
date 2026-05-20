from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from trekking_and_tour_management_system.packages.models import TrekPackage
from trekking_and_tour_management_system.packages.api.serializers import (
    TrekPackageSerializer,
)

from trekking_and_tour_management_system.packages.selectors.package_selectors import (
    get_available_packages,
    search_packages,
    get_all_packages,
)

from trekking_and_tour_management_system.users.permissions import (
    IsAdmin,
)

from rest_framework.permissions import SAFE_METHODS


class TrekPackageViewSet(viewsets.ModelViewSet):

    serializer_class = TrekPackageSerializer

    def get_queryset(self):

        user = self.request.user
        query = self.request.query_params.get("q")

        # admin sees all
        if user.is_authenticated and user.role == "admin":
            queryset = get_all_packages()
        else:
            queryset = get_available_packages()

        if query:
            queryset = search_packages(query)

        return queryset

    def get_permissions(self):

        if self.request.method in SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]

        return [IsAdmin()]
    
    