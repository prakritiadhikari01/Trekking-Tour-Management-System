from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from trekking_and_tour_management_system.packages.models import TrekPackage
from trekking_and_tour_management_system.users.models import User

from .serializers import UserSerializer, TrekPackageSerializer

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return User.objects.all()

        return User.objects.filter(id=user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)
    
class TrekPackageViewSet(viewsets.ModelViewSet):
    queryset = TrekPackage.objects.all()
    serializer_class = TrekPackageSerializer

    def get_queryset(self):
        user = self.request.user

        # customers see available packages
        if user.role == "customer":
            return TrekPackage.objects.filter(available=True)

        return TrekPackage.objects.all()