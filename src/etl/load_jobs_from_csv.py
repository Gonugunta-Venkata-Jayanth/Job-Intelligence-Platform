import pandas as pd
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from src.db.session import SessionLocal, init_db
from src.db import models
def get_or_create_company(db: Session, name: str) -> models.Company:
    company = db.query(models.Company).filter_by(name=name).first()
    if company:
        return company
    company = models.Company(name=name);db.add(company);db.commit();db.refresh(company)
    return company
def get_or_create_location(db: Session, raw_location: str) -> models.Location:
    loc = db.query(models.Location).filter_by(raw_location=raw_location).first()
    if loc:
        return loc
    loc = models.Location(raw_location=raw_location);db.add(loc);db.commit();db.refresh(loc)
    return loc
def parse_date_safe(value: Optional[str]):
    if not value or pd.isna(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None
def load_jobs_from_csv(csv_path: str):
    init_db()
    df = pd.read_csv(csv_path)
    db: Session = SessionLocal()
    try:
        for _, row in df.iterrows():
            company = get_or_create_company(db, str(row["company"]))
            location = get_or_create_location(db, str(row["location"]))
            job = models.Job(title=str(row["title"]),source=str(row.get("source", "csv_import")),url=str(row.get("url", None)),company_id=company.id,location_id=location.id,description=str(row.get("description", "")),min_salary=float(row["min_salary"]) if not pd.isna(row["min_salary"]) else None,max_salary=float(row["max_salary"]) if not pd.isna(row["max_salary"]) else None,currency=str(row.get("currency", None)) if not pd.isna(row.get("currency", None)) else None,posted_date=parse_date_safe(row.get("posted_date")),)
            db.add(job)
        db.commit()
        print(f"Imported {len(df)} jobs from {csv_path}")
    finally:
        db.close()
if __name__ == "__main__":
    load_jobs_from_csv("data/raw/sample_jobs.csv")