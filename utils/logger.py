import logging
from datetime import datetime

# create logger
logging.basicConfig(
    filename="data/etl_logs.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)