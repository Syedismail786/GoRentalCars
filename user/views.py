# user/views.py
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserSignupForm
from bookings.models import Booking
from cars.models import Car

CustomUser = get_user_model()


# User Signup View
def user_signup(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # ✅ Redirects to login after signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserSignupForm()

    return render(request, 'login_signup.html', {'form': form, 'form_type': 'signup'})


# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login_signup.html', {'form': form, 'form_type': 'login'})


# User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# User Profile (Protected)
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


# Home View (List all cars)
def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})


# Car Search View
def car_search(request):
    query = request.GET.get('query', '')
    cars = Car.objects.filter(name__icontains=query) if query else Car.objects.all()
    return render(request, 'home.html', {'cars': cars, 'query': query})


# About Us Page
def about_us(request):
    return render(request, 'about_us.html')


# Services Page
def services(request):
    return render(request, 'services.html')


# Contact Page
def contact(request):
    return render(request, 'contact.html')


# Terms and Conditions Page
def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


# Privacy Policy Page
def privacy_policy(request):
    return render(request, 'privacy_policy.html')


# My Trips (Protected)
@login_required
def my_trips(request):
    trips = Booking.objects.filter(user=request.user).select_related('car')

    trip_data = []
    for trip in trips:
        total_hours = (trip.dropoff_date - trip.pickup_date).total_seconds() / 3600
        trip_data.append({
            'id': trip.id,
            'car': trip.car,
            'pickup_date': trip.pickup_date.date(),
            'total_hours': round(total_hours),
            'total_amount': trip.total_amount,
            'payment_status': trip.payment_status,
        })

    return render(request, 'my_trips.html', {'trips': trip_data})


# Trip Details (Protected)
@login_required
def trip_details(request, booking_id):
    trip = get_object_or_404(Booking, id=booking_id, user=request.user)
    total_hours = (trip.dropoff_date - trip.pickup_date).total_seconds() / 3600
    return render(request, 'trip_details.html', {
        'trip': trip,
        'total_hours': round(total_hours),
    })
