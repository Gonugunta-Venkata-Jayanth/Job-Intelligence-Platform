"""Generic text/salary helpers used by the scrapers and the ETL loader."""
import html
import random
import re
import time
from typing import Optional, Tuple

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

_TAG_RE = re.compile(r"<[^>]+>")
_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F2FF]+")
_WS_RE = re.compile(r"\s+")
_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)*)\s*([kKmM]|lpa|LPA|lakh|lakhs)?")


def random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def polite_sleep(min_s: float = 1.0, max_s: float = 3.0) -> None:
    """Sleep a random amount of time between requests (anti rate-limit)."""
    time.sleep(random.uniform(min_s, max_s))


def clean_text(value: Optional[str]) -> str:
    """Strip HTML tags, HTML entities, emojis and collapse whitespace."""
    if not value:
        return ""
    text = html.unescape(_TAG_RE.sub(" ", str(value)))
    text = _EMOJI_RE.sub(" ", text)
    return _WS_RE.sub(" ", text).strip()


def _to_number(raw: str, unit: Optional[str]) -> float:
    number = float(raw.replace(",", ""))
    unit = (unit or "").lower()
    if unit == "k":
        number *= 1_000
    elif unit == "m":
        number *= 1_000_000
    elif unit in {"lpa", "lakh", "lakhs"}:
        number *= 100_000
    return number


def parse_salary_range(value: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    """Parse free-text salary strings such as ``"$80k - $100k"`` or ``"8-12 LPA"``.

    Returns ``(min, max)``; both are ``None`` when nothing numeric is found.
    A single number is returned as both min and max.
    """
    if not value:
        return None, None
    matches = _NUM_RE.findall(str(value))
    numbers = []
    # A unit given only once ("8-12 LPA") applies to every number.
    shared_unit = next((u for _, u in reversed(matches) if u), None)
    for raw, unit in matches:
        try:
            numbers.append(_to_number(raw, unit or shared_unit))
        except ValueError:
            continue
    numbers = [n for n in numbers if n > 0]
    if not numbers:
        return None, None
    return min(numbers[:2]), max(numbers[:2])
