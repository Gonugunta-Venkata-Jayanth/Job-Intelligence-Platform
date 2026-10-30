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

- **Job scrapers** – `src/scrapping/` pulls live postings from the free public [Remotive](https://remotive.com/api-documentation) and [Arbeitnow](https://www.arbeitnow.com/blog/job-board-api) APIs (retries, rotating user agent, polite delays, de-duplication, HTML cleaning) and writes them as a CSV in the loader's format.
- **ETL from CSV** – `src/etl/load_jobs_from_csv.py <csv>` reads job postings with pandas and normalises them into `companies`, `locations` and `jobs` tables (get-or-create helpers in `src/db/crud.py`).
- **Synthetic data generator** – `src/etl/generate_synthetic_jobs.py` augments `data/raw/sample_jobs.csv` into a larger demo dataset (`jobs_synthetic_large.csv`, 20,000 rows by default) by varying titles, companies, locations and salaries.
- **Rule-based NLP skill extraction** – `src/nlp_ml/skill_extractor.py` matches 30+ technical skills (Python, SQL, Spark, Airflow, AWS, Snowflake, Docker, Kubernetes, Power BI …) with compiled regular expressions and links them to jobs through a `job_skills` table.
- **Salary prediction** – `src/nlp_ml/salary_model_train.py` trains a `TfidfVectorizer` (1–2 grams) + `RandomForestRegressor` pipeline on title + description + location to predict average salary; `salary_model_inference.py` fills `salary_pred_min` / `salary_pred_max` (±15 % band) for jobs without a posted salary.
- **REST API** – FastAPI service split into `routers/jobs.py` and `routers/skills.py`: search with location and skill filters, pagination, job detail, skill list and top skills, with interactive Swagger docs.
- **Tests** – pytest suite (`tests/`) covering the CSV loader, skill tagging, every API endpoint and the helpers.
- **Streamlit dashboard** – KPI cards, sidebar filters (text search, locations, skills, actual vs predicted salary), skill frequency chart, salary chart and a jobs table.
- **Power BI report** – `powerbi/Job_Insights_Report.pbix` (PDF export in `screenshots and pdf/`).
- **Configurable storage** – SQLite by default, any SQLAlchemy URL (e.g. PostgreSQL) via `DATABASE_URL`.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| Data processing | pandas, NumPy |
| Database / ORM | SQLAlchemy, SQLite (default); PostgreSQL works with any SQLAlchemy driver (e.g. `psycopg2-binary`, installed separately) |
| NLP | Regex-based skill dictionary |
| Machine learning | scikit-learn (TF-IDF + Random Forest), joblib |
| API | FastAPI, Pydantic v2, Uvicorn |
| Dashboards | Streamlit, Power BI |
| Scraping | requests (Remotive and Arbeitnow JSON APIs) |
| Testing | pytest, FastAPI TestClient |

## Architecture

```mermaid
flowchart LR
    S[Scrapers<br/>Remotive, Arbeitnow] --> A
    A[CSV: scraped / sample / synthetic] --> B[ETL<br/>load_jobs_from_csv.py]
    B --> DB[(SQL database<br/>SQLite / PostgreSQL)]
    DB --> C[Skill extractor<br/>regex NLP]
    C -->|job_skills| DB
    DB --> D[Salary model training<br/>TF-IDF + RandomForest]
    D --> M[[salary_model.joblib]]
    M --> E[Salary inference]
    E -->|salary_pred_min / max| DB
    DB --> API[FastAPI<br/>/jobs, /skills]
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
│   ├── api/            # FastAPI app (main.py), routers/jobs.py, routers/skills.py, schemas
│   ├── config/         # Settings (PROJECT_NAME, ENV, DATABASE_URL)
│   ├── dashboards/     # Streamlit dashboard (streamlit_app.py)
│   ├── db/             # SQLAlchemy models, session, crud helpers, schema.sql, seed script
│   ├── etl/            # CSV loader and synthetic data generator
│   ├── nlp_ml/         # Skill extractor, salary features, model training & inference
│   ├── scrapping/      # Remotive + Arbeitnow API scrapers and run_all_scrapers CLI
│   └── utils/          # Logging, text cleaning and salary-parsing helpers
├── tests/              # pytest suite
├── data/
│   ├── raw/            # sample_jobs.csv, jobs_synthetic_large.csv
│   └── models/         # salary_model.joblib
├── powerbi/            # Job_Insights_Report.pbix
├── architecture/       # Target-state architecture diagram
├── screenshots and pdf/# API, dashboard and Power BI screenshots
├── db_schema.md · model_performance.md · scraping_strategy.md · deployment_steps.md
└── requirements.txt · requirements-dev.txt
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
pip install psycopg2-binary
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/job_intel"
```

Tables are created automatically on first run (`Base.metadata.create_all`).

### 3. Run the pipeline

Run every command from the repository root:

```bash
# Optional: scrape live postings (Remotive + Arbeitnow) into a CSV, add --load to import it
python -m src.scrapping.run_all_scrapers --query "data engineer" --max-jobs 50

# Load jobs (default data/raw/sample_jobs.csv, or pass any CSV in the same layout)
python -m src.etl.load_jobs_from_csv
python -m src.etl.load_jobs_from_csv data/raw/scraped_jobs.csv

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

Run the tests with:

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

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
| GET | `/jobs/{job_id}` | One job (404 if missing) | – |
| GET | `/skills` | All skills, alphabetical | – |
| GET | `/skills/top` | Most frequent skills with job counts | `limit` (1–100, default 20) |

Example:

```bash
curl "http://127.0.0.1:8000/jobs?q=data%20engineer&location=hyderabad&skill=python&limit=5"
curl "http://127.0.0.1:8000/skills/top?limit=10"
```

## Results

- Screenshots of the running API (`/docs`, `/health`, `/jobs`, `/skills/top`) and the Streamlit dashboard are in [`screenshots and pdf/`](screenshots%20and%20pdf/), along with a PDF export of the Power BI report.
- Salary model ([`model_performance.md`](model_performance.md)): on the 20,000-row synthetic dataset the TF-IDF + Random Forest model scored MAE 112,276, RMSE 139,563 and R² 0.580 on a 4,000-row hold-out. The data is synthetic (generated from 3 sample jobs), so this demonstrates the pipeline, not real-world accuracy; the committed `salary_model.joblib` is a tiny demo model trained on 3 rows.

## Future Work

- Schedule the scrapers and add more sources (see [`scraping_strategy.md`](scraping_strategy.md))
- Train the salary model on real postings with salaries and add structured features (seniority, skills, city)
- Add EDA / modelling notebooks
- Add Alembic migrations, Docker setup and CI
- Job recommendations and LLM-based job summarisation

## License

MIT – see [LICENSE](LICENSE).

## Author

**GV Jayanth** – [GitHub @Gonugunta-Venkata-Jayanth](https://github.com/Gonugunta-Venkata-Jayanth) · [LinkedIn](https://www.linkedin.com/in/gv-jayanth)
