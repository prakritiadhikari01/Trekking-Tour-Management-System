# core/validators.py
import re
from django.core.exceptions import ValidationError

def validate_rating(value):

    if value < 1 or value > 5:
        raise ValidationError(
            "Rating must be between 1 and 5."
        )

def validate_phone_number(value):

    pattern = r"^\+?[0-9]{7,15}$"

    if not re.match(
        pattern,
        value,
    ):
        raise ValidationError(
            "Invalid phone number."
        )

def validate_positive_amount(value):

    if value <= 0:
        raise ValidationError(
            "Amount must be positive."
        )