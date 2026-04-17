CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temperature REAL,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed REAL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);