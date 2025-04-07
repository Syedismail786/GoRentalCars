from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal
from .forms import BookingForm
from .models import Car, Booking

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)  # ✅ fix here

        if form.is_valid():
            pickup_date = form.cleaned_data['pickup_date']
            dropoff_date = form.cleaned_data['dropoff_date']
            booking_type = form.cleaned_data['booking_type']
            license_image = form.cleaned_data['license_image']  # ✅ fetch uploaded file

            if pickup_date.tzinfo is None:
                pickup_date = timezone.make_aware(pickup_date)
            if dropoff_date.tzinfo is None:
                dropoff_date = timezone.make_aware(dropoff_date)

            if pickup_date < timezone.now():
                messages.error(request, "Pickup date cannot be in the past.")
                return render(request, 'booking_form.html', {'car': car, 'form': form})

            if dropoff_date <= pickup_date:
                messages.error(request, "Drop-off date must be later than pickup date.")
                return render(request, 'booking_form.html', {'car': car, 'form': form})

            if booking_type == 'Hourly' and dropoff_date.date() != pickup_date.date():
                messages.error(request, "For hourly bookings, the drop-off date must be within the same day.")
                return render(request, 'booking_form.html', {'car': car, 'form': form})

            if booking_type == 'Daily' and dropoff_date.date() == pickup_date.date():
                messages.error(request, "For daily bookings, the drop-off date must be different from the pickup date.")
                return render(request, 'booking_form.html', {'car': car, 'form': form})

            overlapping_bookings = Booking.objects.filter(
                car=car,
                dropoff_date__gt=pickup_date,
                pickup_date__lt=dropoff_date
            )

            if overlapping_bookings.exists():
                messages.error(request, "Sorry, this car is already booked for the selected time range.")
                return render(request, 'booking_form.html', {'car': car, 'form': form})

            duration_hours = Decimal((dropoff_date - pickup_date).total_seconds()) / Decimal(3600)

            if booking_type == 'Daily':
                total_days = (duration_hours // 24) + (Decimal(1) if duration_hours % 24 > 0 else Decimal(0))
                total_amount = car.price_per_day * total_days
            else:
                total_amount = car.price_per_hour * duration_hours

            booking = Booking.objects.create(
                user=request.user,
                car=car,
                pickup_date=pickup_date,
                dropoff_date=dropoff_date,
                booking_type=booking_type,
                total_amount=total_amount,
                license_image=license_image,  # ✅ include this
            )

            return redirect(reverse('payments:payment_page', kwargs={'booking_id': booking.id}))
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'car': car, 'form': form})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_list.html', {'bookings': bookings})


def terms_conditions(request):
    return render(request, 'terms_conditions.html')


