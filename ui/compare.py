import streamlit as st
from utils.database import read_query

def get_latest_city_data(df, city):
    city_df = df[df["city"] == city].sort_values("observed_at")
    return city_df.iloc[-1]  # ONLY latest record


def compare_page():

    st.title("⚖️ Compare Weather (Latest Data Only)")

    df = read_query("SELECT * FROM bi.weather_observations")

    if df.empty:
        st.warning("No data available. Please fetch weather first.")
        return

    cities = df["city"].unique()

    city1 = st.selectbox("Select City 1", cities)
    city2 = st.selectbox("Select City 2", cities)

    if city1 and city2:

        d1 = get_latest_city_data(df, city1)
        d2 = get_latest_city_data(df, city2)

        st.markdown("---")
        st.subheader("📍 Latest Weather Snapshot Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(city1)
            st.write(f"🕒 Time: {d1['observed_at']}")
            st.metric("🌡️ Temperature", f"{round(d1['temperature'], 1)} °C")
            st.metric("💧 Humidity", f"{d1['humidity']} %")
            st.metric("🌍 Pressure", f"{d1['pressure']} hPa")
            st.metric("🌬️ Wind Speed", f"{d1['wind_speed']} m/s")

        with col2:
            st.subheader(city2)
            st.write(f"🕒 Time: {d2['observed_at']}")
            st.metric("🌡️ Temperature", f"{round(d2['temperature'], 1)} °C")
            st.metric("💧 Humidity", f"{d2['humidity']} %")
            st.metric("🌍 Pressure", f"{d2['pressure']} hPa")
            st.metric("🌬️ Wind Speed", f"{d2['wind_speed']} m/s")

        # ---------------- CLEAN INSIGHTS ----------------
        st.markdown("---")
        st.subheader("📌 Insights")

        temp_diff = round(abs(d1["temperature"] - d2["temperature"]), 1)
        humidity_diff = abs(d1["humidity"] - d2["humidity"])

        if d1["temperature"] > d2["temperature"]:
            st.write(f"🔥 {city1} is hotter than {city2}")
        else:
            st.write(f"🔥 {city2} is hotter than {city1}")

        st.write(f"🌡️ Temperature Difference: {temp_diff}°C")
        st.write(f"💧 Humidity Difference: {humidity_diff}%")