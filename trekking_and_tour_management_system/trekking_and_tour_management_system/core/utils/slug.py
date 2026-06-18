#trekking_and_tour_management_system/core/utils/slug.py
from django.utils.text import slugify


def generate_unique_slug(model_class, value):
    base_slug = slugify(value)
    slug = base_slug

    counter = 1

    while model_class.objects.filter(
        slug=slug
    ).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug