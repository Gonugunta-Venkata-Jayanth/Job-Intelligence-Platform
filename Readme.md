#  Job Intelligence Platform  
### AI-Powered Job Market Analytics | FastAPI • Streamlit • NLP • ML • Power BI

The **Job Intelligence Platform** is an end-to-end intelligent analytics system that processes tech job postings, extracts in-demand skills using NLP, predicts salary ranges using machine learning, and provides insights through APIs and dashboards.

This project integrates **Data Engineering + NLP + Machine Learning + API Development + BI Visualization** in a single production-style pipeline.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-API-green?logo=fastapi" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?logo=streamlit" />
  <img src="https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikitlearn" />
  <img src="https://img.shields.io/badge/Power%20BI-Analytics-F2C811?logo=powerbi" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql" />
  <img src="https://img.shields.io/github/license/darksun003/job-intel-platform?color=blue" />
  <img src="https://img.shields.io/github/last-commit/darksun003/job-intel-platform?logo=github" />
</p>


## 🔥 Key Capabilities

| Feature | Description |
|--------|-------------|
| 📥 ETL Pipeline | Loads raw job postings from CSV into a normalized SQL database |
| 🔍 Smart Skill Extraction (NLP) | Automatically identifies technical skills from job descriptions |
| 💰 Salary Prediction Model | ML model predicts expected salary range for jobs lacking salary info |
| ⚙ REST API Layer | FastAPI backend with interactive Swagger (OpenAPI) |
| 📊 Interactive Dashboards | Streamlit UI + Power BI analytics |
| 🗃 Database | Tables: Jobs, Companies, Locations, Skills, Job-Skills |

> **Dataset:** Demonstration dataset `sample_jobs.csv` is used to show complete workflow end to end.

---

## 🏗 System Architecture
```
CSV → ETL → SQL Database
↓
┌─────────────┐
│ Salary Model│◀──── NLP Skill Extractor
└─────────────┘
↓
┌──────────────┬───────────────┬───────────────┐
```

---

## 📂 Project Structure
```
job-intel-platform/
│
├── src/
│ ├── db/ # Database models + session management
│ ├── etl/ # CSV ingestion / preprocessing pipeline
│ ├── nlp_ml/ # NLP skill extraction + ML salary model
│ ├── api/ # FastAPI routes & Pydantic schemas
│ └── dashboards/ # Streamlit user interface
│
├── data/
│ ├── raw/ # job CSV inputs
│ └── models/ # trained ML models (.joblib)
│
├── powerbi/ # Power BI report (.pbix)
└── README.md
```


---

## ⚡ Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python 3 |
| Backend API | FastAPI |
| Dashboard | Streamlit |
| BI Reporting | Power BI |
| ML | scikit-learn |
| NLP | RegEx-based skill extraction |
| Storage | PostgreSQL / SQLite |
| ORM | SQLAlchemy |

---

## 🚀 Getting Started

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt

│ FastAPI API │ Streamlit App │ Power BI │
└──────────────┴───────────────┴───────────────┘
```
### 2️⃣ Load dataset into the database
```
python -m src.etl.load_jobs_from_csv
```
### 3️⃣ Extract skills
```
python -m src.nlp_ml.skill_extractor
```
### 4️⃣ Train salary model
```
python -m src.nlp_ml.salary_model_train
```

Dashboard includes:
```
Job search & filtering
Company-wise job count
Location-wise demand
Top skills analysis
Salary insights
```

🔹 Power BI Analytics
```
Open the .pbix file under the powerbi/ folder to visualize:
Demand by company & location
Skill frequency trends
Salary distributions
Hiring patterns for data roles
```

✨ Outcome
```
The platform demonstrates a complete real-world job intelligence pipeline including:
ETL
NLP skill mining
Salary prediction
Interactive dashboards [powerbi, streamlit]
Fast API for external integrations
```

⚙ Future Enhancements (Roadmap)
```
Real-time job ingestion via APIs
Recommendation system for job seekers
LLM-based job summarization
Deployment on cloud 
```

👤 Author
```
Field	Details
Name	GV Jayanth
Email	📩 jayanth792033@gmail.com
LinkedIn	🔗 https://www.linkedin.com/in/gv-jayanth
GitHub	💻 https://github.com/darksun003
```
