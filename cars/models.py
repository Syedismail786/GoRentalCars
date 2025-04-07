from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cars/')
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])
    transmission = models.CharField(max_length=50, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')])
    seating_capacity = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    def __str__(self):
        return self.name