from django.contrib.auth import get_user_model

User = get_user_model()


def get_total_customers():
    return User.objects.filter(is_staff=False).count()


def get_active_customers():
    return User.objects.filter(bookings__isnull=False).distinct().count()