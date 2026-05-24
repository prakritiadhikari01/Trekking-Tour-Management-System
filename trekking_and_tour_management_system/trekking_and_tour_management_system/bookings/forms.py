from trekking_and_tour_management_system.bookings.models import Booking
from trekking_and_tour_management_system.users import forms


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'tour_package', 'booking_date', 'number_of_people']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }