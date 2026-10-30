from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers import jobs, skills
from src.config.settings import settings
from src.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="Job Intelligence Platform - API layer",
    lifespan=lifespan,
)
app.include_router(jobs.router)
app.include_router(skills.router)


@app.get("/", tags=["system"])
def root():
    return {"message": "Job Intelligence Platform API", "docs_url": "/docs", "health_url": "/health"}


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
