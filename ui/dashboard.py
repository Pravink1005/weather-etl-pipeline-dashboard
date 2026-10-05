import streamlit as st
import pandas as pd
import plotly.express as px

from utils.config import CITIES, CITY_COORDS
from utils.database import read_query
from jobs.pipeline import run_current_pipeline

st.set_page_config(
    page_title="Tamil Nadu Weather",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');

:root {
    --ink: #193b35;
    --muted: #64766e;
    --paper: #f3f4ed;
    --line: #dce3d9;
    --leaf: #173c35;
    --coral: #d66c4a;
    --sun: #efbd62;
}
.stApp {
    background: var(--paper);
    color: var(--ink);
    font-family: 'DM Sans', 'Segoe UI', sans-serif;
}
[data-testid="stHeader"] { background: var(--paper); }
[data-testid="stMainBlockContainer"] { padding-top: 2.2rem; }
[data-testid="stSidebar"] { background: var(--leaf); border-right: 1px solid #315a50; }
[data-testid="stSidebar"] * { color: #f3f4ed; }
[data-testid="stSidebar"] [data-testid="stRadio"] label p { color: #f3f4ed; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: 0.35rem 0.5rem; border-radius: 4px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: #285247; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label:first-child { display: none; }
h1, h2, h3 { color: var(--ink); font-family: 'DM Serif Display', Georgia, serif; }
h2 { margin-top: 0.4rem; }
[data-testid="stMetric"] {
    background: #fffefa;
    border: 1px solid var(--line);
    border-top: 3px solid var(--coral);
    border-radius: 6px;
    padding: 13px 16px;
    box-shadow: 0 5px 16px rgba(25, 59, 53, 0.04);
}
[data-testid="stMetricLabel"] { color: var(--muted); }
[data-testid="stMetricValue"] { color: var(--ink); }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 6px; }
.brand-lockup { display: flex; align-items: center; gap: 12px; padding: 0.6rem 0 1.5rem; border-bottom: 1px solid #315a50; margin-bottom: 1.4rem; }
.brand-mark { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 4px; color: var(--leaf); background: var(--sun); font-size: 0.83rem; font-weight: 700; }
.brand-name { color: #fffefa; font-size: 0.94rem; font-weight: 700; }
.brand-caption { color: #b8ccc1; font-size: 0.65rem; letter-spacing: 0.08em; margin-top: 3px; }
.sidebar-caption { color: #b8ccc1; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; margin: 0.3rem 0 0.55rem; }
.report-hero { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; min-height: 210px; padding: 30px 34px; margin-bottom: 24px; border-radius: 6px; color: #f3f4ed; background: linear-gradient(112deg, #173c35 0%, #245348 72%, #326557 100%); position: relative; overflow: hidden; }
.report-hero:after { content: ''; position: absolute; inset: 0 0 0 auto; width: 27%; background: repeating-linear-gradient(118deg, transparent 0 18px, rgba(239, 189, 98, 0.09) 19px 20px); }
.hero-kicker { color: var(--sun); font-size: 0.74rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; }
.hero-title { color: #fffefa; font-family: 'DM Serif Display', Georgia, serif; font-size: 2.65rem; font-weight: 400; line-height: 1.05; margin: 0; }
.hero-subtitle { color: #d0dfd7; font-size: 0.95rem; margin: 12px 0 0; }
.hero-stamp { z-index: 1; min-width: 205px; padding: 8px 0 8px 20px; border-left: 2px solid var(--coral); }
.hero-stamp-label { color: #b8ccc1; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }
.hero-stamp-value { color: #fffefa; font-size: 1.05rem; font-weight: 600; margin-top: 5px; }
.hero-stamp-note { color: #d0dfd7; font-size: 0.78rem; margin-top: 3px; }
.section-note { color: var(--muted); font-size: 0.84rem; margin: -0.35rem 0 0.75rem; }
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] { padding: 1rem 1rem 2rem; }
    .report-hero { display: block; padding: 24px 20px; }
    .hero-title { font-size: 2rem; }
    .hero-stamp { margin-top: 22px; }
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# DB FUNCTION
# ----------------------------
def get_data(query, params=None):
    return read_query(query, params)


df_all = get_data("SELECT * FROM bi.weather_observations")

if "observed_at" in df_all.columns:
    df_all["observed_at"] = pd.to_datetime(df_all["observed_at"])


# ----------------------------
# MENU
# ----------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand-lockup"><div class="brand-mark">TN</div>'
        '<div><div class="brand-name">MONSOON / 10</div>'
        '<div class="brand-caption">WEATHER OBSERVATORY</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-caption">Workspace</div>', unsafe_allow_html=True)
    menu = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Search", "⚖️ Compare", "🌍 Map", "🧾 Data Explorer"],
        label_visibility="collapsed",
    )
    st.markdown(
        '<div style="margin-top:2rem;color:#b8ccc1;font-size:.72rem;line-height:1.6">'
        'OPEN-METEO<br>POSTGRESQL · HOURLY</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# 🏠 DASHBOARD
# =========================================================
if menu == "🏠 Dashboard":
    if df_all.empty:
        st.markdown(
            '<section class="report-hero"><div><div class="hero-kicker">Tamil Nadu / Field report</div>'
            '<h1 class="hero-title">Weather observatory</h1>'
            '<p class="hero-subtitle">Hourly conditions from across the state.</p></div></section>',
            unsafe_allow_html=True,
        )
        st.info("No observations yet. Run `python -m jobs.pipeline` to load the first weather report.")
    else:
        latest = df_all.sort_values("observed_at").groupby("city").tail(1).copy()
        latest_time_ist = pd.Timestamp(latest["observed_at"].max()).tz_convert("Asia/Kolkata")
        warmest = latest.loc[latest["temperature"].idxmax()]

        st.markdown(
            '<section class="report-hero"><div><div class="hero-kicker">Tamil Nadu / Field report</div>'
            '<h1 class="hero-title">Weather observatory</h1>'
            '<p class="hero-subtitle">A live regional snapshot from ten city stations.</p></div>'
            f'<div class="hero-stamp"><div class="hero-stamp-label">Latest observation</div>'
            f'<div class="hero-stamp-value">{latest_time_ist:%d %b %Y · %I:%M %p}</div>'
            '<div class="hero-stamp-note">Indian Standard Time</div></div></section>',
            unsafe_allow_html=True,
        )

        action_column, note_column = st.columns([1, 4])
        with action_column:
            if st.button("↻ Fetch current weather", type="primary", use_container_width=True):
                with st.spinner("Fetching current conditions for all cities..."):
                    refresh_succeeded = run_current_pipeline()
                if refresh_succeeded:
                    st.session_state["current_refresh_completed"] = True
                    st.rerun()
                else:
                    st.error("Refresh failed. Check `data/etl_logs.log` for details.")
        with note_column:
            st.caption("On demand · Open-Meteo current conditions · typically updated at 15-minute intervals")

        if st.session_state.pop("current_refresh_completed", False):
            st.success("Current weather refreshed for all configured cities.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Stations reporting", latest["city"].nunique())
        col2.metric("Mean temperature", f"{latest['temperature'].mean():.1f} °C")
        col3.metric("Warmest station", warmest["city"], f"{warmest['temperature']:.1f} °C")
        col4.metric("Records collected", f"{len(df_all):,}")

        st.subheader("Temperature across stations")
        st.markdown('<p class="section-note">Latest completed hourly reading · Celsius</p>', unsafe_allow_html=True)
        temperature_chart = px.bar(
            latest.sort_values("temperature"),
            x="temperature",
            y="city",
            orientation="h",
            text="temperature",
            labels={"temperature": "Temperature (°C)", "city": ""},
        )
        temperature_chart.update_traces(
            marker_color="#d66c4a",
            texttemplate="%{x:.1f}°",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}: %{x:.1f} °C<extra></extra>",
        )
        temperature_chart.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=4, r=48, t=6, b=28),
            height=390,
            bargap=0.38,
            showlegend=False,
            font=dict(color="#193b35", family="DM Sans, Segoe UI, sans-serif"),
            xaxis=dict(
                title="Temperature (°C)",
                range=[0, max(40, float(latest["temperature"].max()) + 5)],
                showgrid=True,
                gridcolor="#dce3d9",
                zeroline=False,
            ),
            yaxis=dict(title="", showgrid=False, tickfont=dict(size=13)),
        )
        st.plotly_chart(temperature_chart, use_container_width=True, config={"displayModeBar": False})

        st.subheader("Latest city readings")
        snapshot = latest[[
            "city", "temperature", "humidity", "pressure", "wind_speed", "observed_at"
        ]].copy()
        snapshot["observed_at"] = (
            snapshot["observed_at"]
            .dt.tz_convert("Asia/Kolkata")
            .dt.strftime("%d %b, %I:%M %p")
        )
        snapshot = snapshot.sort_values("city").rename(columns={
            "city": "City",
            "temperature": "Temperature (°C)",
            "humidity": "Humidity (%)",
            "pressure": "Surface pressure (hPa)",
            "wind_speed": "Wind speed (m/s)",
            "observed_at": "Observed (IST)",
        })
        st.dataframe(
            snapshot,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Temperature (°C)": st.column_config.NumberColumn(format="%.1f"),
                "Humidity (%)": st.column_config.NumberColumn(format="%.0f"),
                "Surface pressure (hPa)": st.column_config.NumberColumn(format="%.1f"),
                "Wind speed (m/s)": st.column_config.NumberColumn(format="%.2f"),
            },
        )


# =========================================================
# 🔍 SEARCH (IMPROVED)
# =========================================================
elif menu == "🔍 Search":

    st.subheader("🔍 City Weather Analytics")

    city = st.selectbox("Select City", CITIES)

    df = get_data("""
        SELECT * FROM bi.weather_observations
        WHERE city = :city
        ORDER BY observed_at DESC
        LIMIT 100
    """, {"city": city})

    if not df.empty:

        if "observed_at" in df.columns:
            df["observed_at"] = pd.to_datetime(df["observed_at"])
            df = df.sort_values("observed_at")

        latest = df.iloc[-1]

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

        if "observed_at" in df.columns:
            st.line_chart(df.set_index("observed_at")["temperature"])
        else:
            df["index"] = range(len(df))
            st.line_chart(df.set_index("index")["temperature"])

        st.divider()

        st.subheader("📋 Data")

        st.dataframe(df[[
            "observed_at",
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

        city_params = {
            f"city_{index}": city for index, city in enumerate(cities)
        }
        city_placeholders = ", ".join(f":{name}" for name in city_params)
        df = get_data(f"""
            SELECT * FROM bi.weather_observations
            WHERE city IN ({city_placeholders})
        """, city_params)

        if "observed_at" in df.columns:
            df["observed_at"] = pd.to_datetime(df["observed_at"])

        latest = df.sort_values("observed_at").groupby("city").tail(1)

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

    latest = df_all.sort_values("observed_at").groupby("city").tail(1)

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