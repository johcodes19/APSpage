from django.contrib import admin
from .models import Service, Booking, Order

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'booked_on')
    list_filter = ('service', 'date')
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('booking', 'created_at', 'is_paid')
    list_filter = ('is_paid',)
