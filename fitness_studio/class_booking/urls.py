from django.urls import path

from . import views

urlpatterns = [
       path('<int:slot_id>/book', views.book_slot, name='book_slot'),
       path('', views.get_booking_details, name='get_booking_details')
]