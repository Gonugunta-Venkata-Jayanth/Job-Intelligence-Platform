from typing import Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
import joblib
from src.db.session import engine, SessionLocal, init_db
from src.db import models
MODEL_PATH = "data/models/salary_model.joblib"
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Loaded model from {MODEL_PATH}")
        return model
    except FileNotFoundError:
        print(f"[ERROR] Model file not found at {MODEL_PATH}. "
            f"Train it first with salary_model_train.py.")
        raise
def fetch_jobs_needing_prediction() -> pd.DataFrame:
    init_db()
    query = text(
        """
        SELECT
            j.id,
            j.title,
            j.description,
            l.raw_location,
            j.salary_pred_min,
            j.salary_pred_max
        FROM jobs j
        LEFT JOIN locations l ON j.location_id = l.id
        WHERE j.min_salary IS NULL
        AND j.max_salary IS NULL
        """
    )
    df = pd.read_sql(query, engine)

    def combine_text(row) -> str:
        parts = [
            str(row.get("title") or ""),
            str(row.get("description") or ""),
            str(row.get("raw_location") or ""),
        ]
        return " \n".join(parts)
    if not df.empty:
        df["text"] = df.apply(combine_text, axis=1)
    return df
def update_predictions_in_db(df_preds: pd.DataFrame) -> None:
    db: Session = SessionLocal()
    try:
        for _, row in df_preds.iterrows():
            job_id = int(row["id"])
            avg_pred = float(row["avg_pred"])
            pred_min = avg_pred * 0.85
            pred_max = avg_pred * 1.15
            job = db.query(models.Job).filter_by(id=job_id).first()
            if not job:
                continue
            job.salary_pred_min = pred_min
            job.salary_pred_max = pred_max
        db.commit()
        print(f"Updated predictions for {len(df_preds)} jobs.")
    finally:
        db.close()
def main():
    model = load_model()
    df_jobs = fetch_jobs_needing_prediction()
    if df_jobs.empty:
        print("No jobs found that need salary prediction.")
        return
    print(f"Found {len(df_jobs)} jobs needing predictions.")
    X = df_jobs["text"]
    avg_preds = model.predict(X)
    df_jobs["avg_pred"] = avg_preds
    print("\nSample predictions:")
    print(df_jobs[["id", "title", "avg_pred"]].head())
    update_predictions_in_db(df_jobs)
if __name__ == "__main__":
    main()