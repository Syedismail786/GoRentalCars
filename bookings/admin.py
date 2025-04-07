from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'pickup_date', 'dropoff_date', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'pickup_date', 'dropoff_date')
