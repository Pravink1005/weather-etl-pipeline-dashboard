import sqlite3
from utils.config import DB_PATH

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    city TEXT,
    temperature REAL,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed REAL,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

    conn.commit()
    conn.close()


def load_data(df):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    INSERT INTO weather_data
    (city, temperature, humidity, pressure, wind_speed, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    for _, row in df.iterrows():
        cursor.execute(query, tuple(row))

    conn.commit()
    conn.close()