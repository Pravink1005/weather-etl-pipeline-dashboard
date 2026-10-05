import streamlit as st
from utils.database import read_query

def search_page():

    st.title("🌦️ Weather Analytics Dashboard")

    # ---------------- LOAD DATA ----------------
    df = read_query("SELECT * FROM bi.weather_observations")

    if df.empty:
        st.warning("No data available. Please run scheduler first.")
        return

    # ---------------- CLEAN DATA ----------------
    df["observed_at"] = pd.to_datetime(df["observed_at"])

    # ---------------- CITY DROPDOWN ----------------
    cities = df["city"].unique()
    city = st.selectbox("📍 Select City", cities)

    if city:

        city_df = df[df["city"] == city].sort_values("observed_at").tail(12)

        if len(city_df) < 2:
            st.warning("Not enough data for charts. Wait for more scheduled runs.")
            return

        st.markdown("---")
        st.subheader(f"📊 Last 12 Records - {city}")

        # ---------------- TEMPERATURE ----------------
        st.subheader("🌡️ Temperature Trend")
        st.line_chart(city_df.set_index("observed_at")["temperature"])

        # ---------------- HUMIDITY ----------------
        st.subheader("💧 Humidity Trend")
        st.line_chart(city_df.set_index("observed_at")["humidity"])

        # ---------------- PRESSURE ----------------
        st.subheader("🌍 Pressure Trend")
        st.line_chart(city_df.set_index("observed_at")["pressure"])

        # ---------------- WIND ----------------
        st.subheader("🌬️ Wind Speed Trend")
        st.line_chart(city_df.set_index("observed_at")["wind_speed"])

        # ---------------- TABLE ----------------
        st.subheader("📋 Raw Data")
        st.dataframe(city_df)