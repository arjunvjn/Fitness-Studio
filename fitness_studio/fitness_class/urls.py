from django.urls import path

from . import views

urlpatterns = [
       path('create_class', views.create_fitness_class, name='create_class'),
       path('', views.get_available_classes, name='get_available_classes')
]