from sqlalchemy import (Column, Integer, String, Date, DateTime, Text, Numeric, ForeignKey, UniqueConstraint, func,)
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    jobs = relationship("Job", back_populates="company")
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    raw_location = Column(Text, nullable=True)
    jobs = relationship("Job", back_populates="location")
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=True, index=True)
    source = Column(String(100), nullable=True)
    title = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    posted_date = Column(Date, nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    min_salary = Column(Numeric, nullable=True)
    max_salary = Column(Numeric, nullable=True)
    currency = Column(String(10), nullable=True)
    salary_pred_min = Column(Numeric, nullable=True)
    salary_pred_max = Column(Numeric, nullable=True)
    company = relationship("Company", back_populates="jobs")
    location = relationship("Location", back_populates="jobs")
    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan",)
class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    jobs = relationship("JobSkill", back_populates="skill", cascade="all, delete-orphan",)
class JobSkill(Base):
    __tablename__ = "job_skills"
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    source = Column(String(50), nullable=True)  
    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="jobs")
    __table_args__ = (UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),)