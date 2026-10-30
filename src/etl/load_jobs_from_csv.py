"""Load job postings from a CSV file into the database.

Usage (from the repository root)::

    python -m src.etl.load_jobs_from_csv                                  # data/raw/sample_jobs.csv
    python -m src.etl.load_jobs_from_csv data/raw/jobs_synthetic_large.csv
"""
import argparse
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session

from src.db import models
from src.db.crud import get_or_create_company, get_or_create_location
from src.db.session import SessionLocal, init_db

DEFAULT_CSV = "data/raw/sample_jobs.csv"


def _clean(value) -> Optional[str]:
    """Return ``None`` for missing values instead of the string ``"nan"``."""
    if value is None or (not isinstance(value, str) and pd.isna(value)):
        return None
    value = str(value).strip()
    return value or None


def _to_float(value) -> Optional[float]:
    if value is None or pd.isna(value):
        return None
    return float(value)


def parse_date_safe(value) -> Optional["datetime.date"]:
    value = _clean(value)
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def load_jobs_from_csv(csv_path: str = DEFAULT_CSV) -> int:
    init_db()
    df = pd.read_csv(csv_path)
    db: Session = SessionLocal()
    try:
        for _, row in df.iterrows():
            company = get_or_create_company(db, _clean(row.get("company")) or "Unknown")
            location = get_or_create_location(db, _clean(row.get("location")) or "Unknown")
            job = models.Job(
                title=_clean(row.get("title")) or "Untitled",
                source=_clean(row.get("source")) or "csv_import",
                url=_clean(row.get("url")),
                company_id=company.id,
                location_id=location.id,
                description=_clean(row.get("description")) or "",
                min_salary=_to_float(row.get("min_salary")),
                max_salary=_to_float(row.get("max_salary")),
                currency=_clean(row.get("currency")),
                posted_date=parse_date_safe(row.get("posted_date")),
            )
            db.add(job)
        db.commit()
        print(f"Imported {len(df)} jobs from {csv_path}")
        return len(df)
    finally:
        db.close()


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Load jobs from a CSV into DATABASE_URL.")
    parser.add_argument("csv_path", nargs="?", default=DEFAULT_CSV, help=f"CSV to load (default: {DEFAULT_CSV})")
    args = parser.parse_args(argv)
    load_jobs_from_csv(args.csv_path)


if __name__ == "__main__":
    main()
