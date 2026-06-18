from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.utils import timezone
from trekking_and_tour_management_system.bookings.models import Booking
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from trekking_and_tour_management_system.bookings.utils import calculate_refund_percentage
from trekking_and_tour_management_system.payments.models import Refund
from trekking_and_tour_management_system.core.pagination import DefaultPagination
from .serializers import BookingHistorySerializer, BookingSerializer, BookingCancelSerializer
from django.db.models import Q
from datetime import timedelta

from rest_framework.views import APIView


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
    pagination_class = DefaultPagination
    
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
    
class CancelBookingAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        booking = get_object_or_404(
            Booking,
            id=pk,
            user=request.user
        )

        #  FIX: use booking_status not status
        if booking.booking_status == "CANCELLED":
            return Response({
                "error": "Booking already cancelled"
            }, status=400)

        refund_percentage = calculate_refund_percentage(
            booking.trip_start_date   #  FIXED (was package.start_date)
        )

        #  FIX: total_price (not total_amount)
        refund_amount = (booking.total_price * refund_percentage) / 100

        #  FIX: correct field name
        booking.booking_status = "CANCELLED"
        booking.cancelled_at = timezone.now()
        booking.cancellation_reason = request.data.get("reason", "")
        booking.save()

        refund = Refund.objects.create(
            booking=booking,
            refund_percentage=refund_percentage,
            refund_amount=refund_amount,
            payment_method=request.data.get("payment_method"),
            refund_account=request.data.get("refund_account")
        )

        return Response({
            "message": "Booking cancelled successfully",
            "refund_percentage": refund_percentage,
            "refund_amount": refund_amount
        }, status=200)