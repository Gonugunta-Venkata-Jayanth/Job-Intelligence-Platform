
---

## 📌 4️⃣ `deployment_steps.md`

```md
# 🚀 Deployment Guide – Job Intelligence Platform

This document describes how to deploy the application end-to-end.

---

📦 1. Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/job-intel-platform.git
cd job-intel-platform

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate     
pip install -r requirements.txt

3. Start Database
Local SQLite (default)
✔ Works automatically — no setup

4. Run ETL and Model
python -m src.etl.load_jobs_from_csv data/raw/sample_jobs.csv
python -m src.nlp_ml.skill_extractor
python -m src.nlp_ml.salary_model_inference

5. Run FastAPI Backend
uvicorn src.api.main:app --reload

6. Run Streamlit Dashboard
streamlit run src/dashboards/streamlit_app.py

7. Publish Power BI Dashboard
Connect to database (SQLite/Postgres)
Build visuals
Publish to Power BI Service
Add dashboard link to README