from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('buy/<int:ticket_id>/', views.buy_ticket, name='buy_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('about-support/', views.about_and_support, name='about_support'),
    path('api/ai-assistant/', views.ai_assistant_api, name='ai_assistant_api'),
    path('pay-kaspi/<int:booking_id>/', views.pay_with_kaspi, name='pay_kaspi'),
]
