from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    pickup_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    dropoff_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    license_image = forms.ImageField(required=True)  # ✅ Add this line

    class Meta:
        model = Booking
        fields = ['pickup_date', 'dropoff_date', 'booking_type', 'license_image']  # ✅ Include in fields
