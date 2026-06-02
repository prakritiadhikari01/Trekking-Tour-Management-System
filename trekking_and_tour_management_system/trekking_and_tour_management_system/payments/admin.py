from django.contrib import admin
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking",
        "user",
        "amount",
        "status",
        "transaction_id",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("booking__id", "user__username", "transaction_id")

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking",
        "refund_amount",   # ✅ FIXED
        "status",
        "created_at"
    )

    list_filter = ("status",)
    search_fields = ("booking__id",)