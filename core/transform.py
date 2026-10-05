from datetime import datetime, timezone

import pandas as pd

WEATHER_CODE_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def transform_data(raw_data):
    records = []
    now = datetime.now(timezone.utc)

    for item in raw_data:
        city = item["city"]
        hourly = item.get("hourly")
        if not isinstance(hourly, dict):
            raise ValueError(f"Missing hourly forecast data for {city}")

        times = hourly.get("time")
        if not isinstance(times, list):
            raise ValueError(f"Missing hourly timestamps for {city}")

        values = {
            "temperature": hourly.get("temperature_2m"),
            "humidity": hourly.get("relative_humidity_2m"),
            "pressure": hourly.get("surface_pressure"),
            "wind_speed": hourly.get("wind_speed_10m"),
            "weather_code": hourly.get("weather_code"),
        }
        if any(not isinstance(series, list) or len(series) != len(times)
               for series in values.values()):
            raise ValueError(f"Incomplete hourly weather data for {city}")

        past_indices = [
            index
            for index, timestamp in enumerate(times)
            if _parse_utc_timestamp(timestamp) <= now
        ]
        if not past_indices:
            raise ValueError(f"No completed hourly weather data available for {city}")

        index = past_indices[-1]
        if any(values[key][index] is None for key in values):
            raise ValueError(f"Missing weather measurements for {city}")

        weather_code = int(values["weather_code"][index])
        records.append({
            "city": city,
            "observed_at": _parse_utc_timestamp(times[index]),
            "temperature": values["temperature"][index],
            "humidity": values["humidity"][index],
            "pressure": values["pressure"][index],
            "wind_speed": values["wind_speed"][index],
            "weather_code": weather_code,
            "description": WEATHER_CODE_DESCRIPTIONS.get(
                weather_code, f"Unknown weather (code {weather_code})"
            ),
        })

    return pd.DataFrame(records)


def transform_current_data(raw_data):
    records = []
    field_names = {
        "temperature": "temperature_2m",
        "humidity": "relative_humidity_2m",
        "pressure": "surface_pressure",
        "wind_speed": "wind_speed_10m",
        "weather_code": "weather_code",
    }

    for item in raw_data:
        city = item["city"]
        current = item.get("current")
        if not isinstance(current, dict):
            raise ValueError(f"Missing current weather data for {city}")

        values = {name: current.get(field) for name, field in field_names.items()}
        if current.get("time") is None or any(value is None for value in values.values()):
            raise ValueError(f"Incomplete current weather data for {city}")

        weather_code = int(values["weather_code"])
        records.append({
            "city": city,
            "observed_at": _parse_utc_timestamp(current["time"]),
            "temperature": values["temperature"],
            "humidity": values["humidity"],
            "pressure": values["pressure"],
            "wind_speed": values["wind_speed"],
            "weather_code": weather_code,
            "description": WEATHER_CODE_DESCRIPTIONS.get(
                weather_code, f"Unknown weather (code {weather_code})"
            ),
        })

    return pd.DataFrame(records)


def _parse_utc_timestamp(value):
    timestamp = datetime.fromisoformat(value)
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc)
