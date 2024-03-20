from django.http import JsonResponse
import requests

from django.shortcuts import render

from .view_utils import get_lat_long
from .constants import API_KEY



BASEURL = 'https://api.openweathermap.org/data/3.0/onecall?'

def get_weather_for_ticker(request):
    cities = []
    for zip in zip_code:
        lat, lon, name = get_lat_long(zip)
        if lat:
            cities.append([lat, lon, name])
    weather_data_list = []

    for city in cities:
        lat, lon, name = city
        url = f'{BASEURL}lat={lat}&lon={lon}&exclude=daily,hourly&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()
        weather_data_list.append({'city': name, 'temp': data["current"]['temp'],})

    return JsonResponse({'weather_data_list': weather_data_list})


def current_weather_of_given_city(request):
    error_message = ''
    if request.method == 'GET':
        zip_code = request.GET.get('zip_code')
        if zip_code:
            lat, lon, name = get_lat_long(zip_code)
            if lat:
                url = f"{BASEURL}lat={lat}&lon={lon}&exclude=hourly,minutely&appid={API_KEY}"
                response = requests.get(url)
                data = response.json()
                return render(request, 'weather.html', {'weather_data': data["current"]['temp'], 'city':name})
            else:
                return render(request, 'weather.html', {'error': 'Invalid zip code or location not found'})
        else:
            return render(request, 'weather.html',{'success': 'Please enter zip code'})
    return render(request, 'weather.html',{'error': 'Please enter zip code'})
