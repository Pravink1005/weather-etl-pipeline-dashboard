import requests
from utils.config import API_KEY

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def extract_data(cities):
    data = []
    for city in cities:
        res = fetch_weather(city)
        if res:
            data.append(res)
    return data