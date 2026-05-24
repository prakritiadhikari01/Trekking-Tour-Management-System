from rest_framework import serializers
from bookings.models import Booking
from payments.models import Payment
from django.db.models import Q


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

class BookingHistorySerializer(serializers.ModelSerializer):

    package_title = serializers.CharField(source="package.title", read_only=True)

    payment = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "package_title",
            "travel_date",
            "number_of_people",
            "total_price",
            "booking_status",
            "payment_status",
            "created_at",
            "payment",
        ]

    def get_payment(self, obj):

        payment = Payment.objects.filter(booking=obj).first()

        if not payment:
            return None

        request = self.context.get("request")

        return {
            "payment_id": payment.id,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "khalti_pidx": payment.pidx,
            "invoice_url": request.build_absolute_uri(
                f"/api/payments/invoice/download/{payment.pidx}/"
            ) if payment.pidx else None
        }