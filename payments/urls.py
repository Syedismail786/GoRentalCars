from django.urls import path
from .views import payment_page
from .import views

app_name = "payments"

urlpatterns = [
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment-success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('payment/<int:booking_id>/', payment_page, name='payment_page'),
]
