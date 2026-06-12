from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated


from trekking_and_tour_management_system.users.api.v1.serializers import UserSerializer
from trekking_and_tour_management_system.users.models import User

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self):

        user = self.request.user

        # admin sees all users
        if user.is_authenticated and user.role == "admin":
            return User.objects.all()

        # normal user sees only self
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):

        serializer = self.get_serializer(
            request.user,
        )

        return Response(serializer.data)

