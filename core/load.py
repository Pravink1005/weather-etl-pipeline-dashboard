from pathlib import Path

from sqlalchemy import text

from utils.config import CITIES, CITY_COORDS
from utils.database import get_engine

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "sql" / "create_table.sql"

def create_table():
    with get_engine().begin() as connection:
        connection.exec_driver_sql(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.execute(
            text("""
                INSERT INTO public.dim_city (city, latitude, longitude)
                VALUES (:city, :latitude, :longitude)
                ON CONFLICT (city) DO UPDATE
                SET latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude
            """),
            [
                {
                    "city": city,
                    "latitude": CITY_COORDS[city]["lat"],
                    "longitude": CITY_COORDS[city]["lon"],
                }
                for city in CITIES
            ],
        )


def load_data(df):
    if df.empty:
        return 0

    statement = text("""
        INSERT INTO public.fact_weather (
            city_id, observed_at, temperature, humidity, pressure,
            wind_speed, weather_code, description
        )
        SELECT city_id, :observed_at, :temperature, :humidity, :pressure,
               :wind_speed, :weather_code, :description
        FROM public.dim_city
        WHERE city = :city
        ON CONFLICT (city_id, observed_at) DO UPDATE SET
            temperature = EXCLUDED.temperature,
            humidity = EXCLUDED.humidity,
            pressure = EXCLUDED.pressure,
            wind_speed = EXCLUDED.wind_speed,
            weather_code = EXCLUDED.weather_code,
            description = EXCLUDED.description,
            ingested_at = CURRENT_TIMESTAMP
    """)
    records = df.to_dict(orient="records")
    with get_engine().begin() as connection:
        result = connection.execute(statement, records)
    return result.rowcount