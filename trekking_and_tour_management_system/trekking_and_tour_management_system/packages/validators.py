from django.core.exceptions import ValidationError


def validate_package_price(price):

    if price <= 0:
        raise ValidationError(
            "Package price must be greater than 0."
        )


def validate_guide_price(price):

    if price < 0:
        raise ValidationError(
            "Guide price cannot be negative."
        )