from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.etl.load_jobs_from_csv import load_jobs_from_csv
from src.nlp_ml.skill_extractor import extract_skills_from_text, tag_skills_for_all_jobs
from src.utils.common import clean_text, parse_salary_range

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_jobs.csv"


@pytest.fixture(scope="module")
def client():
    n = load_jobs_from_csv(str(SAMPLE))
    assert n > 0
    tag_skills_for_all_jobs()
    with TestClient(app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_jobs_list_and_filters(client):
    body = client.get("/jobs").json()
    assert body["count"] >= 2
    hyd = client.get("/jobs", params={"location": "hyderabad"}).json()
    assert hyd["count"] >= 1
    assert all("Hyderabad" in j["location"]["raw_location"] for j in hyd["items"])
    py = client.get("/jobs", params={"skill": "python"}).json()
    assert py["count"] == body["count"]  # every sample job mentions Python


def test_job_detail_and_404(client):
    first = client.get("/jobs").json()["items"][0]
    assert client.get(f"/jobs/{first['id']}").json()["title"] == first["title"]
    assert client.get("/jobs/999999").status_code == 404


def test_top_skills(client):
    top = client.get("/skills/top", params={"limit": 3}).json()
    assert len(top) == 3
    assert top[0]["job_count"] >= top[-1]["job_count"]
    assert "Python" in {s["name"] for s in client.get("/skills").json()}


def test_skill_extraction():
    assert {"Python", "SQL", "AWS"} <= extract_skills_from_text("Python, SQL and AWS")


def test_helpers():
    assert parse_salary_range("$80k - $100k") == (80_000, 100_000)
    assert parse_salary_range("8-12 LPA") == (800_000, 1_200_000)
    assert parse_salary_range("") == (None, None)
    assert clean_text("<p>Hi &amp; there</p>") == "Hi & there"
