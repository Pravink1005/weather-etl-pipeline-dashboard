import sys
import os
import streamlit as st
import sqlite3
import pandas as pd
from utils.config import DB_PATH


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def search_page():

    st.title("🌦️ Weather Analytics Dashboard")

    # ---------------- LOAD DATA ----------------
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM weather_data", conn)
    conn.close()

    if df.empty:
        st.warning("No data available. Please run scheduler first.")
        return

    # ---------------- CLEAN DATA ----------------
    df["created_at"] = pd.to_datetime(df["created_at"])

    # ---------------- CITY DROPDOWN ----------------
    cities = df["city"].unique()
    city = st.selectbox("📍 Select City", cities)

    if city:

        city_df = df[df["city"] == city].sort_values("created_at").tail(12)

        if len(city_df) < 2:
            st.warning("Not enough data for charts. Wait for more scheduled runs.")
            return

        st.markdown("---")
        st.subheader(f"📊 Last 12 Records - {city}")

        # ---------------- TEMPERATURE ----------------
        st.subheader("🌡️ Temperature Trend")
        st.line_chart(city_df.set_index("created_at")["temperature"])

        # ---------------- HUMIDITY ----------------
        st.subheader("💧 Humidity Trend")
        st.line_chart(city_df.set_index("created_at")["humidity"])

        # ---------------- PRESSURE ----------------
        st.subheader("🌍 Pressure Trend")
        st.line_chart(city_df.set_index("created_at")["pressure"])

        # ---------------- WIND ----------------
        st.subheader("🌬️ Wind Speed Trend")
        st.line_chart(city_df.set_index("created_at")["wind_speed"])

        # ---------------- TABLE ----------------
        st.subheader("📋 Raw Data")
        st.dataframe(city_df)