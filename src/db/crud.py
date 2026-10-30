"""Database read/write helpers shared by the API, ETL and NLP modules."""
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db import models


# ---------------------------------------------------------------- get-or-create
def get_or_create_company(db: Session, name: str) -> models.Company:
    company = db.query(models.Company).filter_by(name=name).first()
    if company:
        return company
    company = models.Company(name=name)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_or_create_location(db: Session, raw_location: str) -> models.Location:
    loc = db.query(models.Location).filter_by(raw_location=raw_location).first()
    if loc:
        return loc
    loc = models.Location(raw_location=raw_location)
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc


def get_or_create_skill(db: Session, name: str) -> models.Skill:
    skill = db.query(models.Skill).filter_by(name=name).first()
    if skill:
        return skill
    skill = models.Skill(name=name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


# ----------------------------------------------------------------------- jobs
def get_job(db: Session, job_id: int) -> Optional[models.Job]:
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def search_jobs(
    db: Session,
    q: Optional[str] = None,
    location: Optional[str] = None,
    skill: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> Tuple[int, List[models.Job]]:
    """Filter jobs by free text, location and skill. Returns ``(total, page)``."""
    query = db.query(models.Job)
    if location:
        query = query.join(models.Location, isouter=True)
        loc = f"%{location.lower()}%"
        query = query.filter(
            models.Location.raw_location.ilike(loc)
            | models.Location.city.ilike(loc)
            | models.Location.state.ilike(loc)
            | models.Location.country.ilike(loc)
        )
    if skill:
        query = query.join(models.JobSkill).join(models.Skill)
        query = query.filter(models.Skill.name.ilike(f"%{skill.lower()}%"))
    if q:
        text = f"%{q.lower()}%"
        query = query.filter(models.Job.title.ilike(text) | models.Job.description.ilike(text))
    if skill:
        # a job matching several skills must only be counted/returned once
        query = query.distinct()
    total = query.count()
    jobs = query.order_by(models.Job.scraped_at.desc(), models.Job.id.desc()).offset(offset).limit(limit).all()
    return total, jobs


# --------------------------------------------------------------------- skills
def top_skills(db: Session, limit: int = 20):
    """Skills ordered by how many jobs mention them: rows of (id, name, job_count)."""
    return (
        db.query(
            models.Skill.id,
            models.Skill.name,
            func.count(models.JobSkill.job_id).label("job_count"),
        )
        .join(models.JobSkill)
        .group_by(models.Skill.id, models.Skill.name)
        .order_by(func.count(models.JobSkill.job_id).desc(), models.Skill.name)
        .limit(limit)
        .all()
    )


def list_skills(db: Session) -> List[models.Skill]:
    return db.query(models.Skill).order_by(models.Skill.name).all()


def jobs_for_skill(db: Session, skill_name: str, limit: int = 20, offset: int = 0):
    return search_jobs(db, skill=skill_name, limit=limit, offset=offset)
