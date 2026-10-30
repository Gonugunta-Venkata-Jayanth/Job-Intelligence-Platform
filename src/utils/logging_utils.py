"""Small logging helper shared by the ETL, scraping and ML scripts."""
import logging
import os

_DEFAULT_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Return a configured logger.

    The level comes from ``level`` or the ``LOG_LEVEL`` environment variable
    (default ``INFO``). Handlers are only attached once per logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel((level or os.getenv("LOG_LEVEL", "INFO")).upper())
    return logger
