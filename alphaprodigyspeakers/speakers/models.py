# bookings/models.py
from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Adding initial data for services (can be done via Django migrations or the admin interface)
def initialize_services():
    services = [
        {"name": "Executive Public Speaking Training", "description": "High-level training for executives", "price": 500.00},
        {"name": "Personalized Coaching", "description": "One-on-one coaching sessions", "price": 300.00},
        {"name": "Workshops and Seminars", "description": "Group workshops and seminars", "price": 100.00},
        {"name": "Speech Writing and Review", "description": "Professional speech writing and review", "price": 200.00},
    ]
    for service in services:
        Service.objects.create(**service)

initialize_services()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField()
    booked_on = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

