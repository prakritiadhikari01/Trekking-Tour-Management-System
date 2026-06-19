import re
from django.core.exceptions import ValidationError


def validate_rating(value):
    """
    Validate rating between 1 and 5 (inclusive).
    """

    if value is None:
        raise ValidationError("Rating is required.")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValidationError("Rating must be a number.")

    if value < 1 or value > 5:
        raise ValidationError("Rating must be between 1 and 5.")


def validate_phone_number(value):
    """
    Validates international phone numbers (basic production-safe version).
    """

    if not value:
        raise ValidationError("Phone number is required.")

    pattern = r"^\+?[1-9]\d{6,14}$"

    value = str(value).strip()

    if not re.fullmatch(pattern, value):
        raise ValidationError(
            "Invalid phone number format. Use 7–15 digits, optional + prefix."
        )


def validate_positive_amount(value):
    """
    Ensures value is greater than zero.
    """

    if value is None:
        raise ValidationError("Amount is required.")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a number.")

    if value <= 0:
        raise ValidationError("Amount must be greater than zero.")