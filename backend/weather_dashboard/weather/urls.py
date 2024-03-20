from django.urls import path
from . import views

urlpatterns = [
    path('current-weather/', views.current_weather_of_given_city, name='current_weather'),
]