"""Base class for job-board scrapers.

Every scraper returns rows in the same column layout as
``data/raw/sample_jobs.csv`` so the output can be fed straight into
``src.etl.load_jobs_from_csv``.
"""
import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.common import polite_sleep, random_user_agent
from src.utils.logging_utils import get_logger

CSV_COLUMNS = [
    "title", "company", "location", "min_salary", "max_salary", "currency",
    "description", "source", "url", "posted_date",
]


class BaseScraper(ABC):
    """Shared HTTP session (retries, rotating user agent, delays) + de-duplication."""

    source_name: str = "base"

    def __init__(self, timeout: float = 20.0, delay: tuple = (1.0, 2.5), max_retries: int = 3):
        self.timeout = timeout
        self.delay = delay
        self.log = get_logger(f"scraper.{self.source_name}")
        self.session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=1.0,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))
        self._seen_urls: set = set()

    def get_json(self, url: str, params: Optional[dict] = None) -> dict:
        headers = {"User-Agent": random_user_agent(), "Accept": "application/json"}
        resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def sleep(self) -> None:
        polite_sleep(*self.delay)

    def dedupe(self, rows: Iterable[Dict]) -> List[Dict]:
        unique = []
        for row in rows:
            key = row.get("url") or (row.get("title"), row.get("company"))
            if key in self._seen_urls:
                continue
            self._seen_urls.add(key)
            unique.append(row)
        return unique

    @abstractmethod
    def fetch(self, query: str, max_jobs: int = 100) -> List[Dict]:
        """Return a list of job dicts with the keys in ``CSV_COLUMNS``."""

    @staticmethod
    def save_csv(rows: List[Dict], path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({col: row.get(col) for col in CSV_COLUMNS})
        return out
