from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Service, Booking, Order, Review, Profile, User
from .forms import BookingForm, ProfileForm, ReviewForm
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
            send_mail(
                'Booking Confirmation',
                f'Thank you for booking {service.name}. Your booking is confirmed for {booking.date} at {booking.time}.',
                'annetdaisymm@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
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
            send_mail(
                'Booking Confirmation',
                f'Thank you for booking {service.name}. Your booking is confirmed for {booking.date} at {booking.time}.',
                'annetdaisymm@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
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
    logger.info("Profile fetched or created: %s", profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            logger.info("Profile form is valid and saved")
            return redirect('profile')
        else:
            logger.warning("Profile form is not valid: %s", form.errors)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})


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
    booking.status = 'Paid'
    booking.save()
    
    # Send confirmation email
    send_mail(
        'Booking Confirmation',
        f'Thank you for your booking! Your payment for {booking.service.name} has been successfully received.',
        'info@alphaprodigyspeakers.com',
        [booking.user.email],
        fail_silently=False,
    )
    
    return render(request, 'payment_success.html', {'booking': booking})


def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

from django.shortcuts import render
from .models import Service

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

def send_booking_confirmation(user, booking):
    subject = 'Booking Confirmation'
    message = f'Dear {user.username},\n\nThank you for booking {booking.service.name}. Your booking is confirmed for {booking.date} at {booking.time}.\n\nBest regards,\nAlpha Prodigy Speakers'
    from_email = 'your-email@example.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})
