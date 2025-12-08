from pydantic import BaseModel
import os
class Settings(BaseModel):
    PROJECT_NAME: str = "Job Intelligence Platform"
    ENV: str = os.getenv("ENV", "dev")
    DATABASE_URL: str = os.getenv("DATABASE_URL","sqlite:///./job_intel.db")
settings = Settings()