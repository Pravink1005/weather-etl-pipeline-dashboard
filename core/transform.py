import pandas as pd

def transform_data(raw_data):
    records = []

    for item in raw_data:
        try:
            records.append({
                "city": item["name"],
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "wind_speed": item["wind"]["speed"],
                "description": item["weather"][0]["description"]
            })
        except:
            continue

    return pd.DataFrame(records)