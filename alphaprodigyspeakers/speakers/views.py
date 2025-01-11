from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Service, Booking, Order
from .forms import BookingForm

def home_view(request):
    return render(request, 'home.html')  # Updated path

def service_list_view(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    return render(request, 'service_detail.html', {'service': service})

def booking_view(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            return redirect('profile')
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

def profile_view(request):
    # Show user profile and past bookings
    return render(request, 'profile.html')


def order_summary_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    order, created = Order.objects.get_or_create(booking=booking)
    return render(request, 'order_summary.html', {'order': order})
