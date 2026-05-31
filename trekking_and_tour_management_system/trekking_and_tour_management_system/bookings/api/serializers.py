from rest_framework import serializers

from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.payments.models import Payment

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
            "trip_start_date",
            "trip_end_date",
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

    package_title = serializers.CharField(
        source="package.title",
        read_only=True
    )

    guide_name = serializers.CharField(
        source="assigned_guide.full_name",
        read_only=True
    )

    payment = serializers.SerializerMethodField()

    class Meta:
        model = Booking

        fields = [
            "id",
            "package_title",
            "trip_start_date",
            "trip_end_date",
            "number_of_people",
            "total_price",
            "booking_status",
            "guide_name",
            "created_at",
            "payment",
        ]

    def get_payment(self, obj):

        payment = Payment.objects.filter(
            booking=obj
        ).first()

        if not payment:
            return None

        request = self.context.get("request")

        return {
            "payment_id": payment.id,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "khalti_pidx": payment.pidx,
            "invoice_url": request.build_absolute_uri(
                f"/api/payments/invoices/{payment.invoice.access_token}/download/"
            ) if getattr(payment, "invoice", None) else None
        }
    
class BookingCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "booking_status", "cancellation_reason"]
        read_only_fields = ["id"]    