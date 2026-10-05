import requests
from utils.config import CITY_COORDS

BASE_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_FIELDS = (
    "temperature_2m",
    "relative_humidity_2m",
    "surface_pressure",
    "wind_speed_10m",
    "weather_code",
)
CURRENT_FIELDS = (
    "temperature_2m",
    "relative_humidity_2m",
    "surface_pressure",
    "wind_speed_10m",
    "weather_code",
)


def fetch_weather(city):
    coordinates = CITY_COORDS.get(city)
    if coordinates is None:
        raise ValueError(f"No coordinates configured for city: {city}")

    params = {
        "latitude": coordinates["lat"],
        "longitude": coordinates["lon"],
        "hourly": ",".join(HOURLY_FIELDS),
        "wind_speed_unit": "ms",
        "timezone": "UTC",
        "past_days": 1,
        "forecast_days": 1,
    }
    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()

    return {"city": city, **response.json()}


def extract_data(cities):
    return [fetch_weather(city) for city in cities]


def fetch_current_weather(city):
    coordinates = CITY_COORDS.get(city)
    if coordinates is None:
        raise ValueError(f"No coordinates configured for city: {city}")

    params = {
        "latitude": coordinates["lat"],
        "longitude": coordinates["lon"],
        "current": ",".join(CURRENT_FIELDS),
        "wind_speed_unit": "ms",
        "timezone": "UTC",
    }
    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()

    return {"city": city, **response.json()}


def extract_current_data(cities):
    return [fetch_current_weather(city) for city in cities]
