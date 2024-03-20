from django.http import JsonResponse
import requests

from django.shortcuts import render

from .view_utils import get_lat_long
from .constants import API_KEY



BASEURL = 'https://api.openweathermap.org/data/3.0/onecall?'

def get_weather_for_ticker(request):
    cities = []
    for zip in zip_code:
        lat, lon = get_lat_long(zip)
        if lat:
            cities.append([lat, lon])
    weather_data_list = []

    for city in cities:
        lat, lon = city
        url = f'{BASEURL}lat={lat}&lon={lon}&exclude=daily,hourly&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()
        weather_data_list.append({'city': city, 'temp': data['main']['temp'], 'description': data['weather'][0]['description']})

    return JsonResponse({'weather_data_list': weather_data_list})


def current_weather_of_given_city(request):
    error_message = ''
    if request.method == 'GET':
        zip_code = request.GET.get('zip_code')
        lat, lon = get_lat_long(zip_code)
        if lat:
            url = f"{BASEURL}lat={lat}&lon={lon}&exclude=hourly,minutely&appid={API_KEY}"
            response = requests.get(url)
            data = response.json()
            print("data here", data["current"]['temp'])
            return render(request, 'weather.html', {'weather_data': data["current"]['temp']})
        else:
            return render(request, 'weather.html', {'error': 'Invalid zip code or location not found'})
    return render(request, 'weather.html',{'error': 'Invalid zip code or location not found'})
