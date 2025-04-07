from django.db import models
from django.conf import settings
from cars.models import Car  # Assuming you have a Car model in the 'cars' app

class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('Hourly', 'Hourly'),
        ('Daily', 'Daily'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_date = models.DateTimeField()
    dropoff_date = models.DateTimeField()
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    license_image = models.ImageField(upload_to='license_images/', null=True, blank=True)  # ✅ ADDED
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.pickup_date} to {self.dropoff_date})"
