📌 Job Intelligence Platform
AI-powered skill & salary insights from real job market data

👤 Author: GV JAYANTH

🚀 Project Overview

The Job Intelligence Platform is an end-to-end data & AI system that automatically collects and analyzes real-world job postings (Data Engineering / Python focus).
It extracts structured data, identifies in-demand skills using NLP, predicts salary ranges using machine learning, and exposes powerful insights through:

🔹 FastAPI backend (Swagger API)
🔹 Streamlit interactive dashboard
🔹 Power BI analytics report

📊 Live Power BI Report:
🔗 https://2djrvf-my.sharepoint.com/:u:/g/personal/darksun_003_2djrvf_onmicrosoft_com/IQC-FNVvA4ieTZYbd5zwHgYqAR6XxuYWyc6FepjhzJ3T1eA?e=LZkdoJ

🧠 Architecture
flowchart LR
    A[Scraper / CSV Loader] --> B[ETL & Cleaning]
    B --> C[NLP Skill Extractor]
    C --> D[Salary Prediction Model]
    D --> DB[(Relational Database)]
    DB --> API[FastAPI Backend]
    DB --> BI[Power BI Analytics]
    API --> ST[Streamlit Dashboard]
    ST --> Users[End Users]
    BI --> Users

🔧 Tech Stack
| Category         | Technology                              |
| ---------------- | --------------------------------------- |
| Backend API      | FastAPI, Uvicorn                        |
| Database         | SQLite (dev) → PostgreSQL (prod-ready)  |
| ORM              | SQLAlchemy                              |
| NLP              | Regex skill mining, stopwords filtering |
| Machine Learning | TF-IDF + RandomForestRegressor          |
| Dashboard        | Streamlit                               |
| BI               | Power BI                                |
| Packaging        | joblib, pandas                          |

📂 Project Structure
job-intel-platform/
│ README.md
│ requirements.txt
│
├─ src/
│  ├─ api/               # FastAPI endpoints
│  ├─ db/                # SQLAlchemy models & DB session
│  ├─ etl/               # Data ingestion (CSV / scraping)
│  ├─ nlp_ml/            # Skill extraction + salary model
│  └─ dashboards/        # Streamlit app
│
├─ data/
│  ├─ raw/               # CSV / scraped files
│  └─ models/            # Saved ML model
│
├─ docs/                 # Documentation (scraping, db schema, ML, deployment)
├─ powerbi/              # PBIX report
└─ architecture/         # Diagram (PNG / PDF)

⚙️ Setup Instructions
1️⃣ Install environment
git clone <repo_url>
cd job-intel-platform
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd "D:\PERSONAL INFO\IOrbit\job-intel-platform" [directory]


2️⃣ Initialize DB and Load Data
$env:DATABASE_URL = "sqlite:///data/jobs.db"
python -m src.etl.load_jobs_from_csv
python -m src.nlp_ml.skill_extractor
python -m src.nlp_ml.salary_model_train
python -m src.nlp_ml.salary_model_inference

3️⃣ Start FastAPI (Swagger UI)
uvicorn src.api.main:app --reload
🔗 Swagger Docs: http://127.0.0.1:8000/docs
🔗 Health Check: http://127.0.0.1:8000/health

4️⃣ Start Streamlit Dashboard
streamlit run src/dashboards/streamlit_app.py
🔗 Dashboard: http://localhost:8501

🌱 Future Improvements
Live job scraping using official APIs (LinkedIn, Indeed, Naukri etc.)
Embedding models for semantic skill extraction (BERT / spaCy)
Real-time pipeline with Airflow
Deploy backend & dashboard to cloud (Render, AWS, Azure)
Automated daily refresh for Power BI