from rest_framework import serializers
from trekking_and_tour_management_system.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["status", "pidx", "transaction_id"]

