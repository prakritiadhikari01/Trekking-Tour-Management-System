from django.utils.text import slugify


def generate_unique_slug(model, value, slug_field="slug"):
    """
    Production-safe unique slug generator.
    """

    base_slug = slugify(value)[:240]
    slug = base_slug

    counter = 1

    while model.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug