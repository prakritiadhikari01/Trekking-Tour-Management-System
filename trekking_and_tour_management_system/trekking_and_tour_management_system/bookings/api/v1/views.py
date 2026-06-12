from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from trekking_and_tour_management_system.bookings.models import Booking
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingHistorySerializer, BookingSerializer, BookingCancelSerializer
from django.db.models import Q
from datetime import timedelta

# LIST + CREATE BOOKINGS
class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show logged-in user's bookings
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        package = serializer.validated_data["package"]

        number_of_people = serializer.validated_data.get(
            "number_of_people",
            1
        )

        trip_start_date = serializer.validated_data[
            "trip_start_date"
        ]

        # Auto calculate end date
        trip_end_date = (
            trip_start_date +
            timedelta(days=package.duration)
        )

        total_price = package.price * number_of_people

        serializer.save(
            user=self.request.user,
            total_price=total_price,
            trip_end_date=trip_end_date,
            booking_status="PENDING",
        )

# RETRIEVE + UPDATE + DELETE
class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure user can only access their own bookings
        return Booking.objects.filter(user=self.request.user)
    
    
class BookingHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingHistorySerializer

    def get_queryset(self):

        qs = Booking.objects.select_related("package").filter(
            user=self.request.user
        )

        
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(package__title__icontains=search) |
                Q(id__icontains=search)
            )

       
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(booking_status=status)

        payment_status = self.request.query_params.get("payment_status")
        if payment_status:
            qs = qs.filter(payment__status=payment_status)

        
        sort = self.request.query_params.get("sort")

        if sort == "oldest":
            qs = qs.order_by("created_at")
        elif sort == "price_high":
            qs = qs.order_by("-total_price")
        elif sort == "price_low":
            qs = qs.order_by("total_price")
        else:
            qs = qs.order_by("-created_at")  # default newest first

        return qs
    
class BookingCancelAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        try:
            booking = self.get_object()

            # ownership check
            if booking.user != request.user:
                return Response(
                    {"detail": "Not allowed"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # already cancelled
            if booking.booking_status == "CANCELLED":
                return Response(
                    {"detail": "Already cancelled"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # update booking
            booking.booking_status = "CANCELLED"
            booking.cancellation_reason = request.data.get("cancellation_reason", "")
            booking.cancelled_at = timezone.now()
            booking.save()

            return Response(
                {
                    "message": "Booking cancelled successfully",
                    "booking_id": booking.id,
                    "status": booking.booking_status
                },
                status=status.HTTP_200_OK
            )

        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )