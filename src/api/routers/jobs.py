from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.api.schemas import JobListResponse, JobOut
from src.db import crud
from src.db.session import get_db

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=JobListResponse)
def list_jobs(
    q: Optional[str] = Query(None, description="Search text in job title / description"),
    location: Optional[str] = Query(None, description="Filter by city/state/country/raw_location"),
    skill: Optional[str] = Query(None, description="Filter by skill name"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    total, jobs = crud.search_jobs(db, q=q, location=location, skill=skill, limit=limit, offset=offset)
    return {"count": total, "items": jobs}


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
