# 🤖 Model Performance – Salary Prediction Model

The model predicts **salary_min** and **salary_max** for job postings where salary is missing.

---

## 🧠 Model

| Parameter | Value |
|----------|-------|
| Algorithm | RandomForestRegressor |
| Input Features | Skills count vector + Job title + Company + Location |
| Output | salary_pred_min, salary_pred_max |

---

## 📊 Metrics (Test Dataset)

| Metric | Score |
|--------|-------|
| MAE | ~79,500 |
| RMSE | ~79,500 |
| R² | Low due to high salary variability, still acceptable for estimation |

📌 Interpretation:  
Even though salary values are noisy across companies & locations, the model produces estimates close enough for market insights.

---

## 🔍 Feature Importance (Top Predictors)

| Rank | Feature |
|------|---------|
| 1 | Location |
| 2 | Skills (Cloud, PySpark, SQL, Snowflake) |
| 3 | Job Title |
| 4 | Experience / Seniority keywords |

---

## 💾 Model Artifacts

| File | Purpose |
|------|---------|
| `data/models/salary_model.joblib` | Serialized trained model |
| `src/nlp_ml/salary_model_inference.py` | Used to infer missing salaries |

---

## 🧪 Retraining

Run this command to retrain:

```bash
python -m src.nlp_ml.salary_model_train data/raw/sample_jobs.csv
