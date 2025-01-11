from django import forms
from .models import Booking,Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']