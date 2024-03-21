from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.current_weather_of_given_city, name='current_weather'),
    path('current-weather/', views.current_weather_of_given_city, name='current_weather'),
    path('get_weather_for_ticker', views.get_weather_for_ticker, name="get_weather_for_ticker"),
]