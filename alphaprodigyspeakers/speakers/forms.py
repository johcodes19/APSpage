from django import forms
from .models import Booking,Review, Service, Profile
from django.contrib.auth.forms import AuthenticationForm

class BookingForm(forms.ModelForm):
    DATE_INPUT_FORMATS = ['%Y-%m-%d']

    # Define time slots
    TIME_SLOTS = [
        ('09:00', '09:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '01:00 PM'),
        ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'),
        ('16:00', '04:00 PM'),
        ('17:00', '05:00 PM'),
    ]

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=DATE_INPUT_FORMATS,
        error_messages={'required': 'Please select a date for the booking.'}
    )
    time = forms.ChoiceField(choices=TIME_SLOTS, error_messages={'required': 'Please select a time slot for the booking.'})

    class Meta:
        model = Booking
        fields = ['date', 'time']
        error_messages = {
            'date': {
                'invalid': 'Enter a valid date in YYYY-MM-DD format.'
            },
            'time': {
                'invalid_choice': 'Select a valid time slot.'
            }
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'preferences']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
