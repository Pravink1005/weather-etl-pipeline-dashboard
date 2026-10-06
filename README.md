# 🌦️ Weather ETL Pipeline with Interactive Dashboard

### Tamil Nadu Weather Analytics (End-to-End Data Engineering Project)

---

## 🚀 Overview

This project is an end-to-end ETL pipeline that collects weather data for Tamil Nadu cities, stores timestamped observations in PostgreSQL, and presents them through an interactive dashboard. Hourly history is collected by the scheduler; the dashboard can also request current conditions on demand.

It simulates a real-world data engineering system with automation, logging, and analytics—focused on **Tamil Nadu city-level weather monitoring**.

---

## 🎯 Key Highlights

* 🔄 Fully automated ETL pipeline (hourly ingestion)
* 🌍 Real-time weather data from API
* 🗄️ Persistent storage with historical tracking
* 📊 Interactive Streamlit dashboard
* ⏰ Scheduled data pipelines (APScheduler)
* 🧾 Logging & monitoring system
* 📈 Time-series analytics

---

## 🏗️ System Architecture

```
        Open-Meteo API
                ↓
        Scheduler (APScheduler)
                ↓
     ETL Pipeline (Python)
   Extract → Transform → Load
                ↓
        PostgreSQL Database
           ↙           ↘
 Streamlit Dashboard  Power BI
```

---

## ⚙️ Tech Stack

| Layer           | Technology        |
| --------------- | ----------------- |
| Language        | Python 🐍         |
| Data Processing | Pandas 📊         |
| API Integration | Requests 🌐       |
| Database        | PostgreSQL 🐘     |
| Scheduling      | APScheduler ⏰     |
| Visualization   | Streamlit 🎨      |
| Logging         | Python Logging 🧾 |

---

## 🌍 Data Source

* Open-Meteo Forecast API (no API key required)
* Hourly historical weather data and on-demand current conditions for configured Tamil Nadu city coordinates
* Temperature, relative humidity, surface pressure, wind speed, and WMO weather code
* Current conditions are typically updated at 15-minute intervals; wind speed is requested in meters per second and timestamps are normalized to UTC

---

## 🧱 Project Structure

```
weather-etl/
│
├── core/              # ETL logic
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│
├── jobs/              # Pipeline & scheduler
│   ├── pipeline.py
│   ├── scheduler.py
│
├── ui/                # Streamlit dashboard
│   ├── dashboard.py
│   ├── search.py
│   ├── compare.py
│
├── utils/             # Config & logging
│   ├── config.py
│   ├── database.py
│   ├── logger.py
│
├── data/              # Generated ETL logs and local data files
├── .streamlit/
│   └── config.toml
├── .env.example
├── .gitignore
│
├── sql/
│   ├── create_table.sql
│   ├── grant_powerbi_reader.sql
│
├── requirements.txt
└── README.md
```

---

## 🔄 ETL Pipeline

### 1️⃣ Extract

* Fetches hourly weather data from Open-Meteo
* Supports multiple Tamil Nadu cities
* Selects the latest completed hourly value for each city

### 2️⃣ Transform

* Cleans and structures raw JSON data
* Extracted fields:

  * City
  * Temperature 🌡️
  * Humidity 💧
  * Pressure 🌍
  * Wind Speed 🌬️
  * Weather Description ☁️

### 3️⃣ Load

* Stores observations in PostgreSQL with UTC observation and ingestion timestamps
* Upserts observations by city and observation timestamp; hourly scheduler records and on-demand current readings share the same history table

---

## ⏰ Automation (Scheduler)

* Runs automatically at defined intervals (default: 1 hour)
* Can be configured for faster testing (e.g., 1 minute)
* The dashboard's **Fetch current weather** button separately requests current conditions on demand

---

## 📊 Dashboard Features

The Streamlit application and Power BI reports use the same PostgreSQL database.

### 🌍 City Selection

* Select and explore any tracked city

### 📈 Time-Series Analytics

* Temperature trends
* Humidity trends
* Pressure trends
* Wind speed trends

### 📋 Data Exploration

* View raw historical records in tabular format

### 🔄 On-Demand Current Weather

* Select **Fetch current weather** on the dashboard to request and store a fresh reading for every configured city.
* The displayed observation time comes from Open-Meteo; current conditions are typically updated at 15-minute intervals, not continuously.

---

## 🧾 Logging & Monitoring

All ETL activities are tracked in:

```
data/etl_logs.log
```

### Logs include:

* Job execution timestamps
* Success/failure status
* Error tracking
* Data insertion details

---

## 🏙️ Supported Cities

* Chennai
* Coimbatore
* Madurai
* Trichy
* Salem
* Tirunelveli
* Erode
* Vellore
* Thoothukudi
* Dindigul

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Pravink1005/weather-etl-pipeline-dashboard.git
cd weather-etl-pipeline-dashboard
```

### 2️⃣ Install Dependencies

```bash
python -m venv .venv
```

In PowerShell, activate the environment and install packages:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3️⃣ Configure Environment

Copy the sample environment file and update the PostgreSQL connection string:

```powershell
Copy-Item .env.example .env
```

Then update `DATABASE_URL` in `.env` with your PostgreSQL instance.

### 4️⃣ Run the app

```powershell
python -m streamlit run ui/dashboard.py
```

---

## 🚀 Production deployment with GitHub Actions

The repository includes a deploy-ready Docker image and GitHub Actions workflows for validation and publishing the app image.

### Docker build

```bash
docker build -t weather-etl-dashboard .
docker run --rm -p 8501:8501 --env-file .env weather-etl-dashboard
```

### GitHub Actions

- CI validation runs on every push and pull request.
- The deploy workflow publishes a Docker image to GitHub Container Registry (GHCR).
- To enable live deployment to a host such as Azure App Service or another container platform, add the required repository secrets and update the workflow target.

The deployment workflow file is stored in `.github/workflows/deploy.yml` and is ready to be connected to your hosting platform.

### 3️⃣ Create and Configure PostgreSQL

Install and start PostgreSQL. In pgAdmin or `psql`, create a database named `weather_etl` and an application login named `weather_app`, and make `weather_app` the database owner. Copy the sample environment file:

```powershell
Copy-Item .env.example .env
```

Set the PostgreSQL host, port, user, and password in `.env` using the `DATABASE_URL` format shown there. Do not commit `.env` or share its credentials.

### 4️⃣ Run the Initial ETL

This creates the PostgreSQL tables and reporting view, then fetches fresh weather data:

```powershell
python -m jobs.pipeline
```

### 5️⃣ Start the Hourly Scheduler

Run this in a separate terminal. It performs the subsequent scheduled fetches hourly:

```powershell
python -m jobs.scheduler
```

### 6️⃣ Launch Streamlit

Run in another terminal:

```powershell
python -m streamlit run ui/dashboard.py
```

### 7️⃣ Connect Power BI

After the initial ETL creates the `bi` schema, connect as a PostgreSQL administrator and run `sql/grant_powerbi_reader.sql` against `weather_etl`. Set a password for `powerbi_reader` in pgAdmin or with `\password powerbi_reader` in `psql`. In Power BI Desktop, choose **Get Data → PostgreSQL database**, enter the server and database, and select `bi.weather_observations`. Start with Import mode.

For Power BI Service refresh against a PostgreSQL server on your PC or local network, configure an On-premises Data Gateway. For hosted PostgreSQL, configure the server's secure connection and credentials instead. SQLite history is not migrated; both dashboards read new observations from PostgreSQL.

---

## 📌 Features at a Glance

* ✔️ Automated data pipeline
* ✔️ Historical weather tracking
* ✔️ Real-time API integration
* ✔️ Interactive analytics dashboard
* ✔️ Logging & monitoring system
* ✔️ Scalable modular architecture

---

## 🧭 What to Do Next

Follow this order to take the project from a local demo to a dependable analytics service:

1. **Verify hourly ingestion.** Run `python -m jobs.scheduler` in a separate terminal, then check `data/etl_logs.log` and confirm new observations appear after the next scheduled run.
2. **Build the Power BI report.** Follow the connection steps above and create report pages for city comparisons and historical trends.
3. **Prepare for deployment.** Move PostgreSQL to a managed host, store credentials in the host's secret manager, deploy the Streamlit app, and run the scheduler as a separate always-on worker.
4. **Improve reliability.** Add API retries, failure alerts, and a dashboard indicator for stale observations before relying on the pipeline operationally.
5. **Extend the analytics.** Add date-range and city filters; explore forecasting only after enough historical observations have accumulated.

---

## 🧠 What This Project Demonstrates

* Data Engineering (ETL pipelines)
* Workflow Automation
* API Integration
* Time-Series Data Handling
* Data Visualization
* Logging & Observability

---

## 👨‍💻 Author

**Pravin Kumar A**
GitHub: https://github.com/Pravink1005

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork and improve
* 📢 Share with others

---

## 📬 Feedback

Suggestions and contributions are always welcome!
