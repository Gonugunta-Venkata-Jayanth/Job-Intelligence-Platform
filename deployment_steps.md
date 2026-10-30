# 🚀 Deployment Guide – Job Intelligence Platform

How to run the application end-to-end. Run every command from the repository root.

## 1. Clone the repository

```bash
git clone https://github.com/Gonugunta-Venkata-Jayanth/Job-Intelligence-Platform.git
cd Job-Intelligence-Platform
```

## 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Database

SQLite (`./job_intel.db`) is used by default and needs no setup; tables are created
automatically. To use PostgreSQL, install a driver and set `DATABASE_URL`:

```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/job_intel"
```

## 4. Ingest data, tag skills, train and run the model

```bash
# optional: pull fresh postings from the public Remotive and Arbeitnow APIs
python -m src.scrapping.run_all_scrapers --query "data engineer" --out data/raw/scraped_jobs.csv

python -m src.etl.load_jobs_from_csv data/raw/sample_jobs.csv   # or any CSV in the same layout
python -m src.nlp_ml.skill_extractor
python -m src.nlp_ml.salary_model_train      # -> data/models/salary_model.joblib
python -m src.nlp_ml.salary_model_inference
```

## 5. Run the FastAPI backend

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## 6. Run the Streamlit dashboard

```bash
streamlit run src/dashboards/streamlit_app.py
```

## 7. Power BI report

Open `powerbi/Job_Insights_Report.pbix`, point its data source at your database
(SQLite via ODBC, or PostgreSQL), refresh, and publish to the Power BI Service if needed.

## 8. Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```
