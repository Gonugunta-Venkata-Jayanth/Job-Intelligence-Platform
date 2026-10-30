from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.api.schemas import SkillOut, SkillWithCount
from src.db import crud
from src.db.session import get_db

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=List[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return crud.list_skills(db)


@router.get("/top", response_model=List[SkillWithCount])
def get_top_skills(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return [
        SkillWithCount(id=row.id, name=row.name, job_count=row.job_count)
        for row in crud.top_skills(db, limit=limit)
    ]
