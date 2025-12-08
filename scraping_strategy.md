# 🕸 Scraping Strategy – Job Intelligence Platform

The scraping pipeline is designed to **collect thousands of job postings daily** while avoiding blocking and maintaining data quality.

---

## 🎯 Target Roles
- Data Engineer
- Python Developer
- Machine Learning Engineer
- Data Scientist
- AI / MLOps / Cloud

---

## 🔁 Scraping Workflow
```
Search Query → Paginated Job Listings → Extract Job URLs → Visit Details Page → Clean → Transform → Save CSV → Load to DB
```

---

## ⚙ Data Extraction Fields

| Field | Source | Fallback |
|-------|--------|----------|
| Title | Listing | Details page |
| Company | Listing | Details page |
| Location | Listing | - |
| Salary | Details page | Predicted if missing |
| Description | Details page | - |
| Skills | NLP-based extraction | - |

---

## 🧠 Skill Extraction (NLP)

Skills are not taken directly from job sites.  
Instead, we parse the **description** using a curated dictionary and fuzzy matching.

📌 Sample detected skills:
```
Python, SQL, Airflow, AWS, Azure, GCP, Docker, Kubernetes, Pandas, PySpark
```

---

## 🛡 Anti-Blocking Strategy

| Technique | Purpose |
|----------|---------|
| Rotating User Agents | Avoid pattern detection |
| Delayed scraping (sleep/random) | Reduce rate limits |
| Retries + exceptions | Ensure reliability |
| Cache duplicate URLs | Avoid redundant requests |

---

## 🧹 Data Cleaning

| Task | Handler |
|------|---------|
| Remove emojis, HTML tags | Regex |
| Normalize salary values | NLP extraction |
| Normalize skills | Mapping + lowercase |

---

## 📦 Storage

📌 Raw data → `data/raw/*.csv`  
📌 Cleaned jobs → Postgres DB (`jobs + skills + job_skills`)  

---

