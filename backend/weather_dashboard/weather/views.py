from django.http import JsonResponse
import requests

from django.shortcuts import render

from .view_utils import get_lat_long, get_lat_long_by_city
from .constants import API_KEY



BASEURL = 'https://api.openweathermap.org/data/3.0/onecall?'

def get_weather_for_ticker(request):
    if request.method == 'GET':
        requested_cities = request.GET.get('cities').split(',')
        weather_data_list = []
        if requested_cities:
            cities = [] 
            for city in requested_cities:
                lat, lon, name = get_lat_long_by_city(city)
                if lat:
                    cities.append([lat, lon, city])
                else:
                    weather_data_list.append({'city': city, 'temp': 'N/A', 'description': 'We could not find for this city'})
            
            for city in cities:
                lat, lon, name = city
                url = f'{BASEURL}lat={lat}&lon={lon}&exclude=daily,hourly,minutely&appid={API_KEY}'
                response = requests.get(url)
                data = response.json()
                weather_data_list.append({'city': name, 'temp': data["current"]['temp'], 'description': data["current"]["weather"][0]["description"]})

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
