from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    travel_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone_number",
            "number_of_people",
            "travel_date",
            "special_request",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "number_of_people": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
            "special_request": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Any special requests?"
            }),
        }