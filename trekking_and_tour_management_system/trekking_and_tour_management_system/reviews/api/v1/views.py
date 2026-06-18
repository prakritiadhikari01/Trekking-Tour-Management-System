from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions
from ...models import Review
from .serializers import ReviewSerializer
from trekking_and_tour_management_system.reviews.api.v1.permissions import IsReviewOwner


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsReviewOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user  

        booking = serializer.validated_data["booking"]

        # check ownership
        if booking.user != user:
            raise ValidationError("This booking does not belong to you.")

        # prevent duplicate review
        if hasattr(booking, "review"):
            raise ValidationError("You already reviewed this booking.")

        serializer.save(
            user=user,
            package=booking.package
        )