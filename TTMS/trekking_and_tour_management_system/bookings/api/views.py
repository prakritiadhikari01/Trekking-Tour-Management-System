from rest_framework import generics, permissions
from bookings.models import Booking
from .serializers import BookingSerializer


# =========================
# LIST + CREATE BOOKINGS
# =========================
class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show logged-in user's bookings
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        package = serializer.validated_data["package"]
        number_of_people = serializer.validated_data.get("number_of_people", 1)

        total_price = package.price * number_of_people

        serializer.save(
            user=self.request.user,
            total_price=total_price
        )


# =========================
# RETRIEVE + UPDATE + DELETE
# =========================
class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure user can only access their own bookings
        return Booking.objects.filter(user=self.request.user)