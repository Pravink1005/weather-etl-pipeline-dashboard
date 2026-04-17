from apscheduler.schedulers.blocking import BlockingScheduler
from core.extract import extract_data
from core.transform import transform_data
from core.load import load_data, create_table
from utils.logger import log_info, log_error
from datetime import datetime

CITIES = [
    "Chennai", "Coimbatore", "Madurai", "Trichy",
    "Salem", "Tirunelveli", "Erode", "Vellore",
    "Thoothukudi", "Dindigul"
]

def job():
    log_info("ETL Job Started")

    print("\n----------------------------")
    print(f"⏰ ETL Job: {datetime.now()}")
    print("----------------------------")

    try:
        create_table()

        raw = extract_data(CITIES)

        if not raw:
            log_error("No data fetched from API")
            return

        clean = transform_data(raw)

        if not clean.empty:
            load_data(clean)
            log_info("Data inserted successfully")
            print("✅ Data inserted successfully")
        else:
            log_error("Transform returned empty data")

    except Exception as e:
        log_error(f"ETL Job Failed: {e}")
        print(f"❌ Error: {e}")


scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=30)

print("🚀 Scheduler started (logging enabled)")
scheduler.start()