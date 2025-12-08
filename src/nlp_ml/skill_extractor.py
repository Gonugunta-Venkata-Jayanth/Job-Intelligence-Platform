from typing import Dict, List, Set
import re
from sqlalchemy.orm import Session
from src.db.session import SessionLocal, init_db
from src.db import models
SKILL_PATTERNS: Dict[str, List[str]] = {
    "Python": [r"\bpython\b"],
    "SQL": [r"\bsql\b"],
    "Java": [r"\bjava\b"],
    "Scala": [r"\bscala\b"],
    "R": [r"\br language\b", r"\b r\b"],  
    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "Scikit-learn": [r"\bscikit[- ]learn\b", r"\bsklearn\b"],
    "TensorFlow": [r"\btensorflow\b"],
    "PyTorch": [r"\bpytorch\b"],
    "Apache Spark": [r"\bspark\b", r"\bapache spark\b"],
    "PySpark": [r"\bpyspark\b"],
    "Hadoop": [r"\bhadoop\b"],
    "Kafka": [r"\bkafka\b"],
    "Airflow": [r"\bairflow\b", r"\bapache airflow\b"],
    "DBT": [r"\bdbt\b"],
    "PostgreSQL": [r"\bpostgresql\b", r"\bpostgres\b"],
    "MySQL": [r"\bmysql\b"],
    "MongoDB": [r"\bmongodb\b"],
    "Snowflake": [r"\bsnowflake\b"],
    "BigQuery": [r"\bbigquery\b"],
    "Redshift": [r"\bredshift\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b"],
    "Azure": [r"\bazure\b", r"\bms azure\b"],
    "GCP": [r"\bgcp\b", r"\bgoogle cloud\b", r"\bgoogle cloud platform\b"],
    "Docker": [r"\bdocker\b"],
    "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "Git": [r"\bgit\b"],
    "Linux": [r"\blinux\b"],
    "Power BI": [r"\bpower bi\b"],
    "Tableau": [r"\btableau\b"],
    "ETL": [r"\betl\b", r"\bextract[- ]transform[- ]load\b"],
    "Data Warehousing": [r"\bdata warehouse\b", r"\bdata warehousing\b"],
}
COMPILED_PATTERNS: Dict[str, List[re.Pattern]] = {
    skill: [re.compile(pat, flags=re.IGNORECASE) for pat in patterns]
    for skill, patterns in SKILL_PATTERNS.items()
}
def extract_skills_from_text(text: str) -> Set[str]:
    if not text:
        return set()
    found: Set[str] = set()
    for skill, patterns in COMPILED_PATTERNS.items():
        for pat in patterns:
            if pat.search(text):
                found.add(skill)
                break
    return found
def get_or_create_skill(db: Session, skill_name: str) -> models.Skill:
    skill = db.query(models.Skill).filter_by(name=skill_name).first()
    if skill:
        return skill
    skill = models.Skill(name=skill_name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill
def tag_skills_for_job(db: Session, job: models.Job) -> int:
    text_parts = [job.title or "", job.description or ""]
    full_text = " \n".join(text_parts)
    skill_names = extract_skills_from_text(full_text)
    if not skill_names:
        return 0
    existing_skill_ids = {
        js.skill_id for js in job.skills
    }
    created_links = 0
    for name in skill_names:
        skill = get_or_create_skill(db, name)
        if skill.id in existing_skill_ids:
            continue
        link = models.JobSkill(
            job_id=job.id,
            skill_id=skill.id,
            source="nlp_extracted",
        )
        db.add(link)
        created_links += 1
    return created_links
def tag_skills_for_all_jobs(batch_size: int = 100) -> None:
    init_db()
    db: Session = SessionLocal()
    try:
        q = db.query(models.Job).order_by(models.Job.id.asc())
        total = q.count()
        print(f"Found {total} jobs in DB. Tagging skills...")
        processed = 0
        offset = 0
        while True:
            jobs_batch = (
                q.offset(offset)
                .limit(batch_size)
                .all()
            )
            if not jobs_batch:
                break
            for job in jobs_batch:
                created = tag_skills_for_job(db, job)
                if created:
                    print(f"Job {job.id}: tagged {created} skills")
                processed += 1
            db.commit()
            offset += batch_size
        print(f"Done. Processed {processed} jobs.")
    finally:
        db.close()
if __name__ == "__main__":
    tag_skills_for_all_jobs(batch_size=100)