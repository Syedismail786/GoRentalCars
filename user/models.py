# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    # You can add any additional fields if needed
    # For example, phone number or address

    def __str__(self):
        return self.username  # Optional, readable string for the user instance
