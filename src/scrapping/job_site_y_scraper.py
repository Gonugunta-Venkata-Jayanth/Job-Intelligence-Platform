"""Scraper for the Arbeitnow free public job-board API
(https://www.arbeitnow.com/blog/job-board-api).

The API has no search parameter, so pages are fetched and filtered locally
by matching every word of the query against title, tags and description.
"""
from datetime import datetime, timezone
from typing import Dict, List

from src.scrapping.base_scraper import BaseScraper
from src.utils.common import clean_text

API_URL = "https://www.arbeitnow.com/api/job-board-api"


class ArbeitnowScraper(BaseScraper):
    source_name = "arbeitnow"

    def __init__(self, max_pages: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.max_pages = max_pages

    @staticmethod
    def _matches(job: Dict, words: List[str]) -> bool:
        haystack = " ".join([
            job.get("title") or "",
            " ".join(job.get("tags") or []),
            job.get("description") or "",
        ]).lower()
        return all(w in haystack for w in words)

    def fetch(self, query: str, max_jobs: int = 100) -> List[Dict]:
        words = [w.lower() for w in query.split() if w.strip()]
        rows: List[Dict] = []
        for page in range(1, self.max_pages + 1):
            payload = self.get_json(API_URL, params={"page": page})
            for job in payload.get("data", []):
                if not self._matches(job, words):
                    continue
                created = job.get("created_at")
                posted = (
                    datetime.fromtimestamp(int(created), tz=timezone.utc).date().isoformat()
                    if created else None
                )
                location = clean_text(job.get("location")) or None
                if job.get("remote"):
                    location = f"{location} (Remote)" if location else "Remote"
                rows.append({
                    "title": clean_text(job.get("title")),
                    "company": clean_text(job.get("company_name")) or "Unknown",
                    "location": location,
                    "min_salary": None,  # Arbeitnow does not publish salaries
                    "max_salary": None,
                    "currency": None,
                    "description": clean_text(job.get("description")),
                    "source": self.source_name,
                    "url": job.get("url"),
                    "posted_date": posted,
                })
                if len(rows) >= max_jobs:
                    break
            if len(rows) >= max_jobs or not (payload.get("links") or {}).get("next"):
                break
            self.sleep()
        self.log.info("Fetched %d jobs for query=%r", len(rows), query)
        return self.dedupe(rows)
