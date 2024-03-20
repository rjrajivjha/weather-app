import requests
from .constants import API_KEY

def get_lat_long(zip_code):
    url = f'https://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&limit=1&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return [data["lat"], data["lon"], data["name"]]
    else:
        return [None, None, None]