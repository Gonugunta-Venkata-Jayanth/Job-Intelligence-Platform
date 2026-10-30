"""Run every scraper and write one CSV in the loader's column layout.

Usage (from the repository root)::

    python -m src.scrapping.run_all_scrapers --query "data engineer" --max-jobs 50
    python -m src.scrapping.run_all_scrapers --query "python" --load   # also load into the DB
"""
import argparse
from typing import List

from src.scrapping.base_scraper import BaseScraper
from src.scrapping.job_site_x_scraper import RemotiveScraper
from src.scrapping.job_site_y_scraper import ArbeitnowScraper
from src.utils.logging_utils import get_logger

log = get_logger("run_all_scrapers")
SCRAPERS = {"remotive": RemotiveScraper, "arbeitnow": ArbeitnowScraper}


def run(query: str, max_jobs: int, sources: List[str]) -> list:
    rows = []
    for name in sources:
        scraper = SCRAPERS[name]()
        try:
            rows.extend(scraper.fetch(query, max_jobs=max_jobs))
        except Exception as exc:  # one failing source should not stop the rest
            log.error("Scraper %s failed: %s", name, exc)
    return rows


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--query", default="data engineer")
    parser.add_argument("--max-jobs", type=int, default=50, help="max jobs per source")
    parser.add_argument("--sources", nargs="+", choices=sorted(SCRAPERS), default=sorted(SCRAPERS))
    parser.add_argument("--out", default="data/raw/scraped_jobs.csv")
    parser.add_argument("--load", action="store_true", help="load the CSV into the database afterwards")
    args = parser.parse_args(argv)

    rows = run(args.query, args.max_jobs, args.sources)
    out = BaseScraper.save_csv(rows, args.out)
    log.info("Saved %d jobs to %s", len(rows), out)
    if args.load and rows:
        from src.etl.load_jobs_from_csv import load_jobs_from_csv
        load_jobs_from_csv(str(out))


if __name__ == "__main__":
    main()
