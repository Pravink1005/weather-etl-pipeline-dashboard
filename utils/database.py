import os
from functools import lru_cache
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from utils.config import DATABASE_URL_ENV

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    database_url = os.getenv(DATABASE_URL_ENV)
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and configure PostgreSQL."
        )
    return create_engine(database_url, pool_pre_ping=True)


def read_query(query, params=None):
    return pd.read_sql_query(text(query), get_engine(), params=params)
