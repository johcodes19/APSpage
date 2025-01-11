from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Service, Booking, Order

def home_view(request):
    return render(request, 'home.html')

def service_list_view(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    return render(request, 'service_detail.html', {'service': service})

def booking_view(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        # Handle booking logic here
        pass
    return render(request, 'booking.html', {'service': service})

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
