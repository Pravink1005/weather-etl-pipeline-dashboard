import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from utils.config import DB_PATH, CITIES, CITY_COORDS

st.set_page_config(page_title="Weather ETL Dashboard", layout="wide")


# ----------------------------
# DB FUNCTION
# ----------------------------
def get_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df


st.title("🌦️ Tamil Nadu Weather Analytics Platform")

df_all = get_data("SELECT * FROM weather_data")

if "timestamp" in df_all.columns:
    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])


# ----------------------------
# MENU
# ----------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🔍 Search", "⚖️ Compare", "🌍 Map", "🧾 Data Explorer"]
)

# =========================================================
# 🏠 DASHBOARD
# =========================================================
if menu == "🏠 Dashboard":

    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df_all))
    col2.metric("Cities", df_all["city"].nunique())
    col3.metric("Avg Temp", f"{df_all['temperature'].mean():.1f} °C")

    st.success("System Running Successfully 🚀")

    st.subheader("🌡️ Latest City Snapshot")

    latest = df_all.sort_values("timestamp").groupby("city").tail(1)

    st.dataframe(latest[[
        "city", "temperature", "humidity", "pressure", "wind_speed"
    ]], use_container_width=True)


# =========================================================
# 🔍 SEARCH (IMPROVED)
# =========================================================
elif menu == "🔍 Search":

    st.subheader("🔍 City Weather Analytics")

    city = st.selectbox("Select City", CITIES)

    df = get_data(f"""
        SELECT * FROM weather_data
        WHERE city = '{city}'
        ORDER BY timestamp DESC
        LIMIT 100
    """)

    if not df.empty:

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")

        latest = df.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🌡️ Temp", f"{latest['temperature']} °C")
        col2.metric("💧 Humidity", f"{latest['humidity']} %")
        col3.metric("🌬️ Wind", f"{latest['wind_speed']} m/s")
        col4.metric("🌍 Pressure", f"{latest['pressure']} hPa")

        st.divider()

        st.subheader("📊 Insights")

        c1, c2, c3 = st.columns(3)

        c1.metric("Max Temp", f"{df['temperature'].max()} °C")
        c2.metric("Min Temp", f"{df['temperature'].min()} °C")
        c3.metric("Avg Temp", f"{df['temperature'].mean():.1f} °C")

        st.divider()

        st.subheader("📈 Trend")

        if "timestamp" in df.columns:
            st.line_chart(df.set_index("timestamp")["temperature"])
        else:
            df["index"] = range(len(df))
            st.line_chart(df.set_index("index")["temperature"])

        st.divider()

        st.subheader("📋 Data")

        st.dataframe(df[[
            "timestamp",
            "temperature",
            "humidity",
            "pressure",
            "wind_speed"
        ]], use_container_width=True)

    else:
        st.warning("No data found")


# =========================================================
# ⚖️ COMPARE (FULL UPGRADE)
# =========================================================
elif menu == "⚖️ Compare":

    st.subheader("⚖️ City Comparison Dashboard")

    cities = st.multiselect("Select Cities", CITIES)

    if len(cities) < 2:
        st.warning("Select at least 2 cities")
    else:

        city_str = ",".join([f"'{c}'" for c in cities])

        df = get_data(f"""
            SELECT * FROM weather_data
            WHERE city IN ({city_str})
        """)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        latest = df.sort_values("timestamp").groupby("city").tail(1)

        st.divider()

        # ----------------------------
        # KPI STYLE COMPARISON
        # ----------------------------
        st.subheader("📊 Latest Weather Comparison")

        cols = st.columns(len(latest))

        for i, (_, row) in enumerate(latest.iterrows()):
            with cols[i]:
                st.metric(
                    label=row["city"],
                    value=f"{row['temperature']} °C",
                    delta=f"Humidity {row['humidity']}%"
                )

        st.divider()

        # ----------------------------
        # BAR CHARTS
        # ----------------------------
        st.subheader("🌡️ Temperature Comparison")
        st.bar_chart(latest.set_index("city")["temperature"])

        st.subheader("💧 Humidity Comparison")
        st.bar_chart(latest.set_index("city")["humidity"])

        st.subheader("🌬️ Wind Speed Comparison")
        st.bar_chart(latest.set_index("city")["wind_speed"])

        st.divider()

        # ----------------------------
        # TABLE
        # ----------------------------
        st.subheader("📋 Latest Snapshot")

        st.dataframe(
            latest[[
                "city",
                "temperature",
                "humidity",
                "pressure",
                "wind_speed"
            ]],
            use_container_width=True
        )


# =========================================================
# 🌍 MAP (FIXED MODERN)
# =========================================================
elif menu == "🌍 Map":

    st.subheader("🌍 Tamil Nadu Weather Heat Map")

    latest = df_all.sort_values("timestamp").groupby("city").tail(1)

    latest["city"] = latest["city"].astype(str).str.strip().str.title()

    latest["lat"] = latest["city"].apply(lambda x: CITY_COORDS.get(x, {}).get("lat"))
    latest["lon"] = latest["city"].apply(lambda x: CITY_COORDS.get(x, {}).get("lon"))

    latest = latest.dropna(subset=["lat", "lon"])

    fig = px.scatter_map(
        latest,
        lat="lat",
        lon="lon",
        color="temperature",
        size="temperature",
        hover_name="city",
        hover_data={
            "temperature": True,
            "humidity": True,
            "pressure": True,
            "wind_speed": True,
            "lat": False,
            "lon": False
        },
        color_continuous_scale="Turbo",
        zoom=6,
        height=650
    )

    # SAFE styling (NO marker.line here)
    fig.update_traces(
        marker=dict(
            sizemode="area",
            opacity=0.8
        )
    )

    st.plotly_chart(fig, width="stretch")

# =========================================================
# 🧾 DATA EXPLORER
# =========================================================
elif menu == "🧾 Data Explorer":

    st.subheader("Full Dataset")

    st.write("Total Records:", len(df_all))
    st.write("Cities:", df_all["city"].nunique())

    st.dataframe(df_all, use_container_width=True)

    st.download_button(
        "Download CSV",
        df_all.to_csv(index=False),
        "weather_data.csv"
    )