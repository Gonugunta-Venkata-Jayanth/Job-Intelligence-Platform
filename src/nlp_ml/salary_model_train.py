import os
from typing import Optional
import pandas as pd
from sqlalchemy import text
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import joblib
from src.db.session import engine, init_db
MODEL_PATH = "data/models/salary_model.joblib"
def load_training_data() -> pd.DataFrame:
    init_db()
    query = text(
                """
        SELECT
            j.id,
            j.title,
            j.description,
            l.raw_location,
            j.min_salary,
            j.max_salary
        FROM jobs j
        LEFT JOIN locations l ON j.location_id = l.id
        WHERE j.min_salary IS NOT NULL
        AND j.max_salary IS NOT NULL
        """
    )
    df = pd.read_sql(query, engine)
    df["min_salary"] = df["min_salary"].astype(float)
    df["max_salary"] = df["max_salary"].astype(float)
    df["avg_salary"] = (df["min_salary"] + df["max_salary"]) / 2.0
    def combine_text(row) -> str:
        parts = [
            str(row.get("title") or ""),
            str(row.get("description") or ""),
            str(row.get("raw_location") or ""),
        ]
        return " \n".join(parts)
    df["text"] = df.apply(combine_text, axis=1)
    df = df.dropna(subset=["avg_salary"])
    df = df[df["text"].str.strip() != ""]
    return df
def train_and_save_model(df: pd.DataFrame, model_path: str = MODEL_PATH) -> None:
    X = df["text"]
    y = df["avg_salary"]
    if len(df) < 20:
        print(f"[WARN] Only {len(df)} training samples available. " f"Model will train, but metrics may be unreliable.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    pipeline = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=5000,
                    stop_words="english",
                ),
            ),
            ("rf", RandomForestRegressor(n_estimators=200, random_state=42)),
        ]
    )
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples...")
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)
    print("\nModel evaluation:")
    print(f"  MAE : {mae:,.2f}")
    print(f"  RMSE: {rmse:,.2f}")
    print(f"  R^2 : {r2:.4f}")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"\nModel saved to: {model_path}")
def main():
    df = load_training_data()
    if df.empty:
        print("[ERROR] No training data found. " "Please ensure jobs have min_salary and max_salary populated.")
        return
    print(f"Loaded {len(df)} rows for training.")
    train_and_save_model(df, MODEL_PATH)
if __name__ == "__main__":
    main()