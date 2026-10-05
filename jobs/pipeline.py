from core.extract import extract_current_data, extract_data
from core.transform import transform_current_data, transform_data
from core.load import load_data, create_table
from utils.logger import log_info, log_error
from utils.config import CITIES

def run_pipeline():
    log_info("ETL Started")

    try:
        create_table()

        raw = extract_data(CITIES)

        if not raw:
            log_error("No data fetched")
            return False

        df = transform_data(raw)

        if not df.empty:
            inserted = load_data(df)
            log_info("ETL Success")
            print(f"ETL succeeded: {inserted} weather observations written")
            return True
        else:
            log_error("Empty transformed data")
            return False

    except Exception as e:
        log_error(f"ETL Failed: {e}")
        print(f"ETL failed: {e}")
        return False


def run_current_pipeline():
    log_info("Current weather refresh started")

    try:
        create_table()
        raw = extract_current_data(CITIES)

        if not raw:
            log_error("No current weather data fetched")
            return False

        df = transform_current_data(raw)
        if df.empty:
            log_error("Empty current weather data")
            return False

        inserted = load_data(df)
        log_info("Current weather refresh succeeded")
        print(f"Current weather refresh succeeded: {inserted} observations written")
        return True
    except Exception as error:
        log_error(f"Current weather refresh failed: {error}")
        print(f"Current weather refresh failed: {error}")
        return False

if __name__ == "__main__":
    raise SystemExit(0 if run_pipeline() else 1)