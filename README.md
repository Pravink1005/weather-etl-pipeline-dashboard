# 🌦️ Weather ETL Pipeline with Interactive Dashboard

### Tamil Nadu Weather Analytics (End-to-End Data Engineering Project)

---

## 🚀 Overview

This project is a **production-style end-to-end ETL pipeline** that collects real-time weather data, processes it, stores historical records, and presents insights through an interactive dashboard.

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
        OpenWeather API
                ↓
        Scheduler (APScheduler)
                ↓
     ETL Pipeline (Python)
   Extract → Transform → Load
                ↓
         SQLite Database
                ↓
        Logging System
         (etl_logs.log)
                ↓
     Streamlit Dashboard
```

---

## ⚙️ Tech Stack

| Layer           | Technology        |
| --------------- | ----------------- |
| Language        | Python 🐍         |
| Data Processing | Pandas 📊         |
| API Integration | Requests 🌐       |
| Database        | SQLite 🗄️        |
| Scheduling      | APScheduler ⏰     |
| Visualization   | Streamlit 🎨      |
| Logging         | Python Logging 🧾 |

---

## 🌍 Data Source

* OpenWeatherMap API
* Real-time weather data for Tamil Nadu cities

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
│   ├── logger.py
│
├── data/
│   ├── weather.db
│   ├── etl_logs.log
│
├── sql/
│   ├── create_table.sql
│
├── requirements.txt
└── README.md
```

---

## 🔄 ETL Pipeline

### 1️⃣ Extract

* Fetches real-time weather data via API
* Supports multiple Tamil Nadu cities

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

* Stores processed data into SQLite
* Maintains **historical time-series records**

---

## ⏰ Automation (Scheduler)

* Runs automatically at defined intervals (default: 1 hour)
* Can be configured for faster testing (e.g., 1 minute)
* Ensures continuous and hands-free data ingestion

---

## 📊 Dashboard Features

### 🌍 City Selection

* Select and explore any tracked city

### 📈 Time-Series Analytics

* Temperature trends
* Humidity trends
* Pressure trends
* Wind speed trends

### 📋 Data Exploration

* View raw historical records in tabular format

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
git clone https://github.com/your-username/weather-etl.git
cd weather-etl
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Key

```python
API_KEY = "your_openweather_api_key"
```

### 4️⃣ Start ETL Scheduler

```bash
python scheduler.py
```

### 5️⃣ Launch Dashboard

```bash
streamlit run dashboard.py
```

---

## 📌 Features at a Glance

* ✔️ Automated data pipeline
* ✔️ Historical weather tracking
* ✔️ Real-time API integration
* ✔️ Interactive analytics dashboard
* ✔️ Logging & monitoring system
* ✔️ Scalable modular architecture

---

## 🔮 Future Enhancements

* 🗺️ Map-based visualization (Geo analytics)
* 🤖 Weather forecasting using ML models
* ⚡ Real-time dashboard auto-refresh
* ☁️ Cloud deployment (AWS / Render)
* 📡 REST API using FastAPI
* 📊 Advanced dashboards with Plotly

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

**Your Name**
GitHub: https://github.com/your-username

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork and improve
* 📢 Share with others

---

## 📬 Feedback

Suggestions and contributions are always welcome!
