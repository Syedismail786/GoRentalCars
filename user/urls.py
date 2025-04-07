# user/urls.py
from django.urls import path
from . import views  # Import views once, not twice

urlpatterns = [

    path('signup/', views.user_signup, name='signup'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('search/', views.car_search, name='car_search'),
    path('about_us/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('terms-conditions/', views.terms_and_conditions, name='terms_conditions'),  # Removed the leading '/'
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('my_trips/', views.my_trips, name='my_trips'),  # My Trips page
    path('trip/<int:booking_id>/', views.trip_details, name='trip_details'),
]
