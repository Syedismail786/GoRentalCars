import razorpay
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



# ✅ Setup Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required

def payment_page(request, booking_id):
    try:
        # Get the booking
        booking = Booking.objects.get(id=booking_id)
        car = booking.car  # Assumes Booking has a ForeignKey to Car

        # Create Razorpay order
        order_data = {
            "amount": int(booking.total_amount * 100),  # amount in paisa
            "currency": "INR",
            "receipt": f"booking_{booking.id}",
            "payment_capture": 1
        }
        order = razorpay_client.order.create(order_data)

        context = {
            "order_id": order["id"],
            "amount": order_data["amount"],
            "currency": order_data["currency"],
            "booking": booking,
            "car_name": car.name,
            "car_image_url": car.image.url if hasattr(car, 'image') and car.image else None,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        }

        return render(request, "payment.html", context)

    except Booking.DoesNotExist:
        return redirect('home')  # You could show a custom 404 too

from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage

@login_required
def payment_success(request, booking_id):
    try:
        # Get the booking object or return a 404 error if not found
        booking = get_object_or_404(Booking, id=booking_id)

        # Set `payment_status` as True after payment is successful
        booking.payment_status = True
        booking.save()

        # Calculate the time difference using pickup and dropoff dates
        if booking.pickup_date and booking.dropoff_date:
            time_difference = booking.dropoff_date - booking.pickup_date

            if booking.booking_type == 'Hourly':  # If the booking is hourly
                total_hours = time_difference.total_seconds() / 3600  # Convert to hours
                total_days = None
            elif booking.booking_type == 'Daily':  # If the booking is daily
                total_hours = None
                total_days = time_difference.days  # Get the number of days
            else:
                total_hours = None
                total_days = None
        else:
            total_hours = None
            total_days = None

        # Get car image URL (make sure the image exists)
        car_image = booking.car.image if booking.car.image else None
        car_image_url = car_image.url if car_image else None

        # Render the HTML email template
        subject = "Payment Successful - GoRentalCars"
        html_message = render_to_string(
            'payment_success_email.html',  # Path to your HTML email template
            {
                'username': booking.user.username,
                'booking_id': booking.id,
                'car_name': booking.car.name,
                'car_image_url': car_image_url,
                'pickup_date': booking.pickup_date,
                'dropoff_date': booking.dropoff_date,
                'total_amount': booking.total_amount,
                'total_hours': total_hours,
                'total_days': total_days,
            }
        )

        # Optionally, send a plain text version for email clients that don't support HTML
        text_message = strip_tags(html_message)  # Converts HTML to plain text

        # Create the email
        email = EmailMultiAlternatives(
            subject,
            text_message,  # Plain text part
            settings.DEFAULT_FROM_EMAIL,  # Sender email
            [booking.user.email],  # Recipient email
        )

        # Attach the car image (if exists)
        if car_image:
            # Open the image using PIL to get MIME type
            with Image.open(car_image.path) as img:
                mime_type = f"image/{img.format.lower()}"
            with open(car_image.path, 'rb') as f:
                email.attach(car_image.name, f.read(), mime_type)

        # Attach the HTML version of the email
        email.attach_alternative(html_message, "text/html")

        # Send the email
        email.send()

        # Add context for rendering the success page
        context = {
            "booking": booking,
            "car_image_url": car_image_url,
            "total_hours": total_hours,
            "total_days": total_days,
        }

        return render(request, "payment_success.html", context)

    except Booking.DoesNotExist:
        # Handle case when booking with the given ID doesn't exist
        return redirect('home')  # Redirect to home or any other page


# Redirect to home or any other page
def payment_failed(request):
    return render(request, 'payment_failed.html')
