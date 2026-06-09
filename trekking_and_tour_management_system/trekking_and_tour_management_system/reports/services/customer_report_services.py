from django.contrib.auth import get_user_model
from reports.selectors.booking_selector import Booking
from django.db.models import Count

User = get_user_model()

def generate_customer_report():
    total_customers = User.objects.filter(is_staff=False).count()

    active_customers = (
        Booking.objects.values("user")
        .distinct()
        .count()
    )

    top_customers = (
        Booking.objects.values(
            "user__id",
            "user__name",
            "user__email",
        )
        .annotate(total_bookings=Count("id"))
        .order_by("-total_bookings")[:5]
    )

    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "top_customers": list(top_customers),
    }