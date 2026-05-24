from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trekking_and_tour_management_system.users.permissions import IsGuide


class GuideDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsGuide
    ]

    def get(self, request):

        return Response({
            "message": "Welcome Guide",
            "assigned_tours": [],
        })