from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "package",
            "full_name",
            "email",
            "phone_number",
            "number_of_people",
            "travel_date",
            "special_request",
            "total_price",
            "booking_status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "total_price",
            "booking_status",
            "created_at",
        ]