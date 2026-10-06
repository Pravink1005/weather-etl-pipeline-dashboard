import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone as pytz_timezone

from core.extract import extract_data
from core.transform import transform_data
from core.load import load_data, create_table
from utils.logger import log_info, log_error
from utils.config import CITIES


def get_scheduler_interval_hours():
    value = os.getenv("SCHEDULER_INTERVAL_HOURS", "1")
    try:
        hours = int(value)
    except (TypeError, ValueError):
        hours = 1
    return max(1, hours)


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

    except Exception as exc:
        log_error(f"ETL Job Failed: {exc}")
        print(f"❌ Error: {exc}")


def create_scheduler():
    scheduler = BlockingScheduler(timezone=pytz_timezone("Asia/Kolkata"))
    scheduler.add_job(job, "interval", hours=get_scheduler_interval_hours())
    return scheduler


if __name__ == "__main__":
    scheduler = create_scheduler()
    print(f"🚀 Scheduler started (runs every {get_scheduler_interval_hours()} hour(s))")
    scheduler.start()
