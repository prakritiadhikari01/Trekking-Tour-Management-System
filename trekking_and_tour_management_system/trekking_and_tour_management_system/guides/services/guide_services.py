from django.contrib.auth import get_user_model
from django.db import transaction

from trekking_and_tour_management_system.guides.models import Guide

User = get_user_model()


@transaction.atomic
def create_guide_by_admin(
    email,
    full_name,
    phone_number,
    experience,
    languages,
):
    if User.objects.filter(email=email).exists():
        raise ValueError("User already exists")

    user = User.objects.create_user(
        email=email,
        password=None,
        name=full_name,
        role="guide",
        must_change_password=True,
    )

    user.set_unusable_password()
    user.save(update_fields=["password"])

    guide = Guide.objects.create(
        user=user,
        full_name=full_name,
        phone_number=phone_number,
        experience=experience,
        languages=languages,
        is_verified=True,
    )

    return guide