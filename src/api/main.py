from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.config.settings import settings
from src.db.session import init_db, get_db
from src.db import models
from src.api.schemas import JobOut, JobListResponse, SkillWithCount
app = FastAPI( title=settings.PROJECT_NAME, version="0.1.0", description="Job Intelligence Platform - API layer",)
@app.on_event("startup")
def on_startup():
    init_db()
@app.get("/", tags=["system"])
def root():
    return {"message": "Job Intelligence Platform API", "docs_url": "/docs", "health_url": "/health",}
@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
@app.get("/jobs", response_model=JobListResponse, tags=["jobs"],)
def list_jobs( q: Optional[str] = Query(None, description="Search text in job title / description"), location: Optional[str] = Query(None, description="Filter by city/state/country/raw_location"),
    skill: Optional[str] = Query(None, description="Filter by skill name"), limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db),):
    query = db.query(models.Job)
    if location:
        query = query.join(models.Location, isouter=True)
    if skill:
        query = query.join(models.JobSkill).join(models.Skill)
    if q:
        ilike = f"%{q.lower()}%"
        query = query.filter(
            models.Job.title.ilike(ilike) | models.Job.description.ilike(ilike)
        )
    if location:
        ilike_loc = f"%{location.lower()}%"
        query = query.filter((models.Location.raw_location.ilike(ilike_loc)) | (models.Location.city.ilike(ilike_loc)) | (models.Location.state.ilike(ilike_loc)) | (models.Location.country.ilike(ilike_loc)))
    if skill:
        ilike_skill = f"%{skill.lower()}%"; query = query.filter(models.Skill.name.ilike(ilike_skill))
    total = query.count()
    jobs = (query.order_by(models.Job.scraped_at.desc()).offset(offset).limit(limit).all())
    return {"count": total, "items": jobs}
@app.get(
    "/skills/top",
    response_model=List[SkillWithCount],
    tags=["skills"],
)
def get_top_skills(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    from sqlalchemy import func
    q = (db.query(models.Skill.id,models.Skill.name,func.count(models.JobSkill.job_id).label("job_count"),).join(models.JobSkill).group_by(models.Skill.id, models.Skill.name)
        .order_by(func.count(models.JobSkill.job_id).desc()).limit(limit))
    rows = q.all()
    return [
        SkillWithCount(id=row.id, name=row.name, job_count=row.job_count)
        for row in rows
    ]