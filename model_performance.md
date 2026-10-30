# 🤖 Model Performance – Salary Prediction Model

The model estimates a job's **average salary**; `salary_model_inference.py` turns that
into `salary_pred_min` / `salary_pred_max` (−15 % / +15 %) for jobs without a posted salary.

## 🧠 Model

| Parameter | Value |
|-----------|-------|
| Pipeline | `TfidfVectorizer(ngram_range=(1, 2), max_features=5000, stop_words="english")` → `RandomForestRegressor(n_estimators=200, random_state=42)` |
| Input feature | One text field: job **title + description + raw location** (`src/nlp_ml/salary_feature_engineering.py`) |
| Target | `avg_salary = (min_salary + max_salary) / 2` |
| Split | 80 / 20 `train_test_split(random_state=42)` |
| Output | `salary_pred_min = 0.85 × prediction`, `salary_pred_max = 1.15 × prediction` |

Skills, company and seniority are **not** separate features; they only influence the
model through the words they contribute to the TF-IDF text.

## 📊 Metrics

Both runs below were produced by running `python -m src.nlp_ml.salary_model_train`
(scikit-learn 1.9.1, Python 3.12) against a database loaded with the stated data.

| Training data | Train / test rows | MAE | RMSE | R² |
|---------------|-------------------|-----|------|----|
| `job_intel.db` as committed (4 jobs with salaries) | 3 / 1 | 79,500 | 79,500 | undefined (1 test row) |
| `data/raw/jobs_synthetic_large.csv` (20,000 synthetic jobs) | 16,000 / 4,000 | 112,276 | 139,563 | 0.580 |

Salaries are in INR.

- The numbers previously listed here (MAE ≈ RMSE ≈ 79,500) came from the first setup:
  with a single test row, MAE and RMSE are identical by definition and R² cannot be
  computed, so those numbers say nothing about model quality.
- The committed `data/models/salary_model.joblib` is that tiny 3-row model
  (61-term vocabulary). It demonstrates the pipeline only.
- The 20,000-row dataset is generated from the 3 sample jobs by
  `src/etl/generate_synthetic_jobs.py` with randomised titles, locations and salaries,
  so its R² reflects how much of that random variation the text explains. It is **not**
  a measure of real-world accuracy. The resulting model (~70 MB) is not committed.

## 💾 Model Artifacts

| File | Purpose |
|------|---------|
| `data/models/salary_model.joblib` | Serialised pipeline (demo model, see above) |
| `src/nlp_ml/salary_feature_engineering.py` | Builds the text feature and target for train and inference |
| `src/nlp_ml/salary_model_train.py` | Trains, prints MAE / RMSE / R², saves the model |
| `src/nlp_ml/salary_model_inference.py` | Fills predictions for jobs without salaries |

## 🧪 Retraining

Training reads every job in `DATABASE_URL` that has both salaries. To reproduce the
20,000-row run in a fresh database:

```bash
export DATABASE_URL=sqlite:///./synthetic.db
python -m src.etl.load_jobs_from_csv data/raw/jobs_synthetic_large.csv
python -m src.nlp_ml.salary_model_train --model-path data/models/salary_model_synthetic.joblib
```
