from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Service, Booking, Order, Review, Profile, User
from .forms import BookingForm, ProfileForm, ReviewForm
from django.contrib import messages
import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from .utils import send_booking_confirmation_email
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import FAQ
from django.shortcuts import render, get_object_or_404
import logging
import pytz
from datetime import datetime
from django.shortcuts import render
from .models import Service
import os.path
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from datetime import timedelta
from django.shortcuts import redirect

def home_view(request):
    return render(request, 'home.html')  # Updated path

def service_list_view(request):
    services = Service.objects.all().order_by('name')
    paginator = Paginator(services, 10)  # Show 10 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'service_list.html', {'page_obj': page_obj})

def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'service_detail.html', {'service': service, 'form': form})


def booking_view(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'service': service, 'form': form})

    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile, 'bookings': bookings})


def order_summary_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    order, created = Order.objects.get_or_create(booking=booking)
    return render(request, 'order_summary.html', {'order': order})


reverse

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_success', args=[booking_id])),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancelled'))},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": booking.service.name,
                        "sku": "item",
                        "price": str(booking.service.price),
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": str(booking.service.price),
                    "currency": "USD"},
                "description": f"Payment for {booking.service.name}"}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    redirect_url = link.href
                    return redirect(redirect_url)
        else:
            return render(request, 'payment_error.html', {"error": payment.error})
    else:
        return render(request, 'payment.html', {'booking': booking})

def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if 'paymentId' in request.GET and 'PayerID' in request.GET:
        payment_id = request.GET['paymentId']
        payer_id = request.GET['PayerID']
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            booking.status = 'Paid'
            booking.is_paid = True
            booking.save()
            
            # Send confirmation email
            send_booking_confirmation(booking.user, booking)
            send_admin_notification(booking)
            add_event_to_google_calendar(booking)
            
            return render(request, 'payment_success.html', {'booking': booking})
        else:
            booking.status = 'Payment Failed'
            booking.save()
            return render(request, 'payment_error.html', {"error": "Payment failed."})
    return render(request, 'payment_error.html', {"error": "Payment details not found."})

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

def send_booking_confirmation(user, booking):
    subject = 'Booking Confirmation'
    message = f'Dear {user.username},\n\nThank you for booking {booking.service.name}. Your booking is confirmed for {booking.date} at {booking.time} (UTC+3).\n\nBest regards,\nAlpha Prodigy Speakers'
    from_email = 'annetdaisymm@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def send_admin_notification(booking):
    subject = 'New Booking Received'
    message = f'New booking for {booking.service.name} by {booking.user.username}\nDate: {booking.date}\nTime: {booking.time} (UTC+3)'
    from_email = 'annetdaisymm@gmail.com'
    recipient_list = ['annetdaisymm@gmail.com']
    send_mail(subject, message, from_email, recipient_list)


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False) 
            user_timezone = pytz.timezone(form.cleaned_data['timezone'])
            nairobi_timezone = pytz.timezone('Africa/Nairobi')
            
            booking_time = datetime.combine(booking.date, booking.time)
            booking_time = user_timezone.localize(booking_time).astimezone(nairobi_timezone)
            
            booking.date = booking_time.date()
            booking.time = booking_time.time()
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully! Please proceed to payment.')
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

# Ensure no email is sent in the above view


def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Service.objects.filter(name__icontains=query)  # Filter services by name containing the query
    return render(request, 'search_results.html', {'query': query, 'results': results})


def search_suggestions_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Service.objects.filter(name__icontains=query).values_list('name', flat=True)
    return JsonResponse({'results': list(results)})

def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})


def add_event_to_google_calendar(booking):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'path_to_client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    
    event = {
        'summary': f'Booking for {booking.service.name}',
        'description': f'Booking by {booking.user.username}',
        'start': {
            'dateTime': booking.date.isoformat() + 'T' + booking.time,
            'timeZone': 'Africa/Nairobi',
        },
        'end': {
            'dateTime': (booking.date + timedelta(hours=1)).isoformat() + 'T' + booking.time,
            'timeZone': 'Africa/Nairobi',
        }
    }
    
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result

# Call this function after a booking is successfully created
#add_event_to_google_calendar(booking)

