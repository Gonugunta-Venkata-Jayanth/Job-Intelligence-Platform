from datetime import date
from sqlalchemy.orm import Session
from src.db.session import SessionLocal, init_db
from src.db import models
def seed():
    init_db()
    db: Session = SessionLocal()
    try:
        company_name = "TechOrbit Analytics"
        company = db.query(models.Company).filter_by(name=company_name).first()
        if not company:
            company = models.Company(name=company_name, website="https://techorbit.example.com");db.add(company);db.commit();db.refresh(company);location = models.Location(city="Hyderabad", state="Telangana", country="India", raw_location="Hyderabad, Telangana, India",)
        db.add(location);db.commit();db.refresh(location);skill_names = ["Python", "SQL", "Pandas", "Apache Spark", "ETL", "AWS"];skills = []
        for name in skill_names:
            skill = db.query(models.Skill).filter_by(name=name).first()
            if not skill:
                skill = models.Skill(name=name);db.add(skill);db.commit();db.refresh(skill);skills.append(skill)
        job = models.Job(external_id="DE-001", source="dummy_seed", title="Data Engineer (Python / Spark)", company_id=company.id, location_id=location.id, posted_date=date.today(), url="https://jobs.example.com/de-001", description=( "We are looking for a Data Engineer with strong Python, SQL, " "Apache Spark, and ETL experience on AWS."), min_salary=800000, max_salary=1400000, currency="INR", salary_pred_min=900000, salary_pred_max=1300000,)
        db.add(job)
        db.commit()
        db.refresh(job)
        for skill in skills:
            js = models.JobSkill(job_id=job.id, skill_id=skill.id, source="seed")
            db.add(js)
        db.commit()
        print(f"Seeded job with id={job.id} and {len(skills)} skills.")
    finally:
        db.close()
if __name__ == "__main__":
    seed()