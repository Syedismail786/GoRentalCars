from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('/terms-conditions/', views.terms_conditions, name='terms_conditions'),


]
