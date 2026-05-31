from rest_framework import viewsets, permissions
from ..models import Review
from .serializers import ReviewSerializer
from trekking_and_tour_management_system.reviews.api.permissions import IsReviewOwner


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsReviewOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)