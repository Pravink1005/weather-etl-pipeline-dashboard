from core.extract import extract_data
from core.transform import transform_data
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
            return

        df = transform_data(raw)

        if not df.empty:
            load_data(df)
            log_info("ETL Success")
        else:
            log_error("Empty transformed data")

    except Exception as e:
        log_error(f"ETL Failed: {e}")

if __name__ == "__main__":
    run_pipeline()