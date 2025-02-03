from django import forms
from .models import Booking,Review, Service, Profile
from django.contrib.auth.forms import AuthenticationForm
from pytz import all_timezones

class BookingForm(forms.ModelForm):
    DATE_INPUT_FORMATS = ['%Y-%m-%d']

    TIME_SLOTS = [
        ('06:00', '06:00 AM'), ('06:30', '06:30 AM'),
        ('07:00', '07:00 AM'), ('07:30', '07:30 AM'),
        ('08:00', '08:00 AM'), ('08:30', '08:30 AM'),
        ('09:00', '09:00 AM'), ('09:30', '09:30 AM'),
        ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'), ('12:30', '12:30 PM'),
        ('13:00', '01:00 PM'), ('13:30', '01:30 PM'),
        ('14:00', '02:00 PM'), ('14:30', '02:30 PM'),
        ('15:00', '03:00 PM'), ('15:30', '03:30 PM'),
        ('16:00', '04:00 PM'), ('16:30', '04:30 PM'),
        ('17:00', '05:00 PM'), ('17:30', '05:30 PM'),
    ]

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=DATE_INPUT_FORMATS,
        error_messages={'required': 'Please select a date for the booking.'}
    )
    time = forms.ChoiceField(choices=TIME_SLOTS, error_messages={'required': 'Please select a time slot for the booking.'})
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in all_timezones], required=True)

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

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if Booking.objects.filter(date=date, time=time).exists():
            raise forms.ValidationError('This time slot is already booked.')
        return cleaned_data


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
        fields = ['avatar', 'bio']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
