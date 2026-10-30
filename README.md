# Job Intelligence Platform

> An end-to-end job-market analytics pipeline: load job postings into a SQL database, tag in-demand skills with NLP, estimate missing salaries with an ML model, and explore it all through a FastAPI service, a Streamlit dashboard and a Power BI report.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/SQLite%20%7C%20PostgreSQL-Database-336791?logo=postgresql&logoColor=white" alt="Database" />
  <img src="https://img.shields.io/badge/Power%20BI-Report-F2C811?logo=powerbi&logoColor=black" alt="Power BI" />
</p>

---

## Features

- **ETL from CSV** – `src/etl/load_jobs_from_csv.py` reads job postings with pandas and normalises them into `companies`, `locations` and `jobs` tables (get-or-create for companies and locations).
- **Synthetic data generator** – `src/etl/generate_synthetic_jobs.py` augments `data/raw/sample_jobs.csv` into a larger demo dataset (`jobs_synthetic_large.csv`, 20,000 rows by default) by varying titles, companies, locations and salaries.
- **Rule-based NLP skill extraction** – `src/nlp_ml/skill_extractor.py` matches 30+ technical skills (Python, SQL, Spark, Airflow, AWS, Snowflake, Docker, Kubernetes, Power BI …) with compiled regular expressions and links them to jobs through a `job_skills` table.
- **Salary prediction** – `src/nlp_ml/salary_model_train.py` trains a `TfidfVectorizer` (1–2 grams) + `RandomForestRegressor` pipeline on title + description + location to predict average salary; `salary_model_inference.py` fills `salary_pred_min` / `salary_pred_max` (±15 % band) for jobs without a posted salary.
- **REST API** – FastAPI service with search, location and skill filters, pagination and a top-skills endpoint, with interactive Swagger docs.
- **Streamlit dashboard** – KPI cards, sidebar filters (text search, locations, skills, actual vs predicted salary), skill frequency chart, salary chart and a jobs table.
- **Power BI report** – `powerbi/Job_Insights_Report.pbix` (PDF export in `screenshots and pdf/`).
- **Configurable storage** – SQLite by default, any SQLAlchemy URL (e.g. PostgreSQL) via `DATABASE_URL`.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| Data processing | pandas, NumPy |
| Database / ORM | SQLAlchemy, SQLite (default), PostgreSQL (`psycopg2-binary`) |
| NLP | Regex-based skill dictionary |
| Machine learning | scikit-learn (TF-IDF + Random Forest), joblib |
| API | FastAPI, Pydantic v2, Uvicorn |
| Dashboards | Streamlit, Power BI |

## Architecture

```mermaid
flowchart LR
    A[sample_jobs.csv / synthetic CSV] --> B[ETL<br/>load_jobs_from_csv.py]
    B --> DB[(SQL database<br/>SQLite / PostgreSQL)]
    DB --> C[Skill extractor<br/>regex NLP]
    C -->|job_skills| DB
    DB --> D[Salary model training<br/>TF-IDF + RandomForest]
    D --> M[[salary_model.joblib]]
    M --> E[Salary inference]
    E -->|salary_pred_min / max| DB
    DB --> API[FastAPI<br/>/jobs, /skills/top]
    DB --> ST[Streamlit dashboard]
    DB --> BI[Power BI report]
```

### Data model

```mermaid
erDiagram
    COMPANIES ||--o{ JOBS : posts
    LOCATIONS ||--o{ JOBS : "located in"
    JOBS ||--o{ JOB_SKILLS : requires
    SKILLS ||--o{ JOB_SKILLS : "tagged on"
    JOBS {
        int id
        string title
        text description
        numeric min_salary
        numeric max_salary
        numeric salary_pred_min
        numeric salary_pred_max
        string currency
        date posted_date
    }
```

Full SQL DDL: [`src/db/schema.sql`](src/db/schema.sql) · ORM models: [`src/db/models.py`](src/db/models.py) · notes: [`db_schema.md`](db_schema.md)

## Project Structure

```
Job-Intelligence-Platform/
├── src/
│   ├── api/            # FastAPI app (main.py) and Pydantic schemas
│   ├── config/         # Settings (PROJECT_NAME, ENV, DATABASE_URL)
│   ├── dashboards/     # Streamlit dashboard (streamlit_app.py)
│   ├── db/             # SQLAlchemy models, session, schema.sql, seed script
│   ├── etl/            # CSV loader and synthetic data generator
│   ├── nlp_ml/         # Skill extractor, salary model training & inference
│   ├── scrapping/      # Scraper modules (placeholders, not implemented yet)
│   └── utils/          # Helpers (placeholders)
├── data/
│   ├── raw/            # sample_jobs.csv, jobs_synthetic_large.csv
│   └── models/         # salary_model.joblib
├── notebooks/          # EDA / NLP / model notebooks (placeholders)
├── powerbi/            # Job_Insights_Report.pbix
├── architecture/       # Target-state architecture diagram
├── screenshots and pdf/# API, dashboard and Power BI screenshots
├── db_schema.md · model_performance.md · scraping_strategy.md · deployment_steps.md
└── requirements.txt
```

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/Gonugunta-Venkata-Jayanth/Job-Intelligence-Platform.git
cd Job-Intelligence-Platform
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. (Optional) choose a database

SQLite (`./job_intel.db`) is used by default. To use PostgreSQL instead:

```bash
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/job_intel"
```

Tables are created automatically on first run (`Base.metadata.create_all`).

### 3. Run the pipeline

Run every command from the repository root:

```bash
# Load jobs (reads data/raw/sample_jobs.csv)
python -m src.etl.load_jobs_from_csv

# Optional: generate the 20k-row synthetic dataset from sample_jobs.csv
python -m src.etl.generate_synthetic_jobs

# Tag skills from titles and descriptions
python -m src.nlp_ml.skill_extractor

# Train the salary model -> data/models/salary_model.joblib
python -m src.nlp_ml.salary_model_train

# Predict salaries for jobs that have none
python -m src.nlp_ml.salary_model_inference
```

You can also insert a single demo record with `python -m src.db.seed_dummy_data`.

> The CSV loader currently reads the path hard-coded in its `__main__` block (`data/raw/sample_jobs.csv`); edit it, or call `load_jobs_from_csv("<path>")`, to load another file.

### 4. Start the API

```bash
uvicorn src.api.main:app --reload
```

Open http://127.0.0.1:8000/docs for Swagger UI.

### 5. Start the dashboard

```bash
streamlit run src/dashboards/streamlit_app.py
```

Open http://localhost:8501.

## API Reference

| Method | Endpoint | Description | Query parameters |
|--------|----------|-------------|------------------|
| GET | `/` | Service info with links to docs and health | – |
| GET | `/health` | Health check | – |
| GET | `/jobs` | Search jobs, newest first; returns `{count, items}` | `q` (title/description text), `location`, `skill`, `limit` (1–100, default 20), `offset` |
| GET | `/skills/top` | Most frequent skills with job counts | `limit` (1–100, default 20) |

Example:

```bash
curl "http://127.0.0.1:8000/jobs?q=data%20engineer&location=hyderabad&skill=python&limit=5"
curl "http://127.0.0.1:8000/skills/top?limit=10"
```

## Results

- Screenshots of the running API (`/docs`, `/health`, `/jobs`, `/skills/top`) and the Streamlit dashboard are in [`screenshots and pdf/`](screenshots%20and%20pdf/), along with a PDF export of the Power BI report.
- Salary-model evaluation recorded by the author is in [`model_performance.md`](model_performance.md). The training script prints MAE, RMSE and R² on a 20 % hold-out split each time it runs; note that the bundled data is small / synthetic, so treat these numbers as a demonstration of the pipeline rather than real-world accuracy.

## Future Work

- Implement the scrapers in `src/scrapping/` (strategy outlined in [`scraping_strategy.md`](scraping_strategy.md)) for real-time ingestion
- Split the API into the planned `routers/jobs.py` and `routers/skills.py` modules and add tests
- Accept a CSV path from the command line in the ETL loader
- Fill in the analysis notebooks and add dedicated salary feature engineering
- Add Alembic migrations, Docker setup and CI
- Job recommendations and LLM-based job summarisation

## License

See [LICENSE](LICENSE).

## Author

**GV Jayanth** – [GitHub @Gonugunta-Venkata-Jayanth](https://github.com/Gonugunta-Venkata-Jayanth) · [LinkedIn](https://www.linkedin.com/in/gv-jayanth)
