from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Service, Booking, Order, Review
from .forms import BookingForm, ReviewForm
import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from .utils import send_booking_confirmation_email
from django.db.models import Q

def home_view(request):
    return render(request, 'home.html')  # Updated path

def service_list_view(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    reviews = Review.objects.filter(service=service)
    if request.user.is_authenticated:
        has_booked = Booking.objects.filter(user=request.user, service=service).exists()
    else:
        has_booked = False
    if request.method == 'POST' and has_booked:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            return redirect('service_detail', service_id=service.id)
    else:
        form = ReviewForm()
    return render(request, 'service_detail.html', {'service': service, 'reviews': reviews, 'form': form, 'has_booked': has_booked})


def booking_view(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            send_booking_confirmation_email(request.user, booking)
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

@login_required 
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'profile.html', {'bookings': bookings})


def order_summary_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    order, created = Order.objects.get_or_create(booking=booking)
    return render(request, 'order_summary.html', {'order': order})


reverse

paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def payment_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
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
    return render(request, 'payment.html', {'booking': booking})


def payment_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.is_paid = True
    booking.save()
    return render(request, 'payment_success.html', {'booking': booking})

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

def search_view(request): 
    query = request.GET.get('q') 
    results = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) 
    return render(request, 'search_results.html', {'results': results, 'query': query})