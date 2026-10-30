"""Scraper for Remotive's free public job API (https://remotive.com/api-documentation).

Remotive's terms ask that you credit Remotive and link back to each job's
URL, and call the API at most a few times a day. The ``source`` column is
set to ``remotive`` and ``url`` keeps the original link.
"""
from typing import Dict, List

from src.scrapping.base_scraper import BaseScraper
from src.utils.common import clean_text, parse_salary_range

API_URL = "https://remotive.com/api/remote-jobs"


class RemotiveScraper(BaseScraper):
    source_name = "remotive"

    def fetch(self, query: str, max_jobs: int = 100) -> List[Dict]:
        payload = self.get_json(API_URL, params={"search": query, "limit": max_jobs})
        rows = []
        for job in payload.get("jobs", [])[:max_jobs]:
            salary_min, salary_max = parse_salary_range(job.get("salary"))
            rows.append({
                "title": clean_text(job.get("title")),
                "company": clean_text(job.get("company_name")) or "Unknown",
                "location": clean_text(job.get("candidate_required_location")) or "Remote",
                "min_salary": salary_min,
                "max_salary": salary_max,
                # Remotive does not state a currency; most listed salaries are USD.
                "currency": "USD" if salary_min else None,
                "description": clean_text(job.get("description")),
                "source": self.source_name,
                "url": job.get("url"),
                "posted_date": (job.get("publication_date") or "")[:10] or None,
            })
        self.log.info("Fetched %d jobs for query=%r", len(rows), query)
        return self.dedupe(rows)
