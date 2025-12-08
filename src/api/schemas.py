from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
class CompanyOut(BaseModel):
    id: int;name: str;website: Optional[str] = None;model_config = ConfigDict(from_attributes=True)
class LocationOut(BaseModel):
    id: int;city: Optional[str] = None;state: Optional[str] = None;country: Optional[str] = None;raw_location: Optional[str] = None;model_config = ConfigDict(from_attributes=True)
class SkillOut(BaseModel):
    id: int;name: str;model_config = ConfigDict(from_attributes=True)
class JobBase(BaseModel):
    title: str;source: Optional[str] = None;url: Optional[str] = None
class JobOut(JobBase):
    id: int;company: Optional[CompanyOut] = None;location: Optional[LocationOut] = None;posted_date: Optional[date] = None;scraped_at: Optional[datetime] = None
    min_salary: Optional[float] = None;max_salary: Optional[float] = None;currency: Optional[str] = None;salary_pred_min: Optional[float] = None;salary_pred_max: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)
class JobListResponse(BaseModel):
    count: int;items: List[JobOut]
class SkillWithCount(SkillOut):
    job_count: int
