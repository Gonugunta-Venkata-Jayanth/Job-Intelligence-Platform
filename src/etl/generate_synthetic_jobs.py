import math
import random
from pathlib import Path
import numpy as np
import pandas as pd
SRC_PATH = Path("data/raw/sample_jobs.csv")
OUT_PATH = Path("data/raw/jobs_synthetic_large.csv")
TARGET_ROWS = 20000  # change to 10000, 30000 etc. if you want
TITLE_COLS = ["title", "job_title", "role"]
COMPANY_COLS = ["company", "company_name"]
LOCATION_COLS = ["location", "location_name", "city"]
DESC_COLS = ["description", "job_description"]
SAL_MIN_COLS = ["salary_min", "min_salary"]
SAL_MAX_COLS = ["salary_max", "max_salary"]
SAL_RAW_COLS = ["salary", "salary_raw"]
LOCATIONS_POOL = ["Bangalore, India", "Hyderabad, India", "Chennai, India", "Pune, India", "Mumbai, India", "Delhi, India","Remote, India",]
TITLE_PREFIXES = ["", "Junior", "Senior", "Lead", "Associate", "Principal"]
TITLE_SUFFIXES = ["", "Engineer", "Developer", "Specialist", "Consultant", "Analyst"]
def find_col(df: pd.DataFrame, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None
def augment_row(row, title_col, company_col, location_col,
                sal_min_col, sal_max_col, sal_raw_col, desc_col):
    if title_col:
        base_title = str(row[title_col]) if pd.notna(row[title_col]) else "Data Engineer"
        prefix = random.choice(TITLE_PREFIXES)
        suffix = random.choice(TITLE_SUFFIXES)
        new_title = base_title
        if random.random() < 0.7:
            new_title = base_title.replace("Engineer", "Engineering").replace("Developer", "Development")
        parts = []
        if prefix and random.random() < 0.7:
            parts.append(prefix)
        parts.append(base_title)
        if suffix and random.random() < 0.5 and suffix not in base_title:
            parts.append(suffix)
        new_title = " ".join(parts)
        row[title_col] = new_title
    if company_col and pd.notna(row[company_col]):
        c = str(row[company_col])
        endings = ["", " Pvt Ltd", " Technologies", " Solutions", " Labs", " Systems"]
        if random.random() < 0.5:
            row[company_col] = c.split("-")[0].strip()  # remove noise
        if random.random() < 0.3:
            row[company_col] = row[company_col] + random.choice(endings)
    if location_col:
        if random.random() < 0.8:
            row[location_col] = random.choice(LOCATIONS_POOL)
    base = None
    if sal_min_col and sal_min_col in row and pd.notna(row[sal_min_col]):
        try:
            base = float(row[sal_min_col])
        except Exception:
            base = None
    if base is None and sal_raw_col and sal_raw_col in row and pd.notna(row[sal_raw_col]):
        txt = str(row[sal_raw_col])
        nums = [s for s in txt.replace("LPA", "").replace("₹", "").replace(",", " ").split() if s.replace(".", "").isdigit()]
        if nums:
            try:
                base = float(nums[0]) * 100000
            except Exception:
                base = None
    if base is None:
        base = random.randint(400000, 1800000)
    factor = 1 + random.uniform(-0.2, 0.2)
    sal_min = max(250000, int(base * factor))
    sal_max = sal_min + random.randint(100000, 800000)
    if sal_min_col:
        row[sal_min_col] = sal_min
    if sal_max_col:
        row[sal_max_col] = sal_max
    if not sal_min_col and not sal_max_col and sal_raw_col:
        row[sal_raw_col] = f"{sal_min//100000}-{sal_max//100000} LPA"
    if desc_col and pd.notna(row[desc_col]):
        desc = str(row[desc_col])
        extras = ["Experience with cloud platforms (AWS/Azure/GCP).", "Hands-on with Docker and CI/CD pipelines.", "Strong communication and stakeholder management skills.", "Comfortable working in Agile/Scrum environments.","Exposure to big data tools like Spark/Hadoop is a plus.",] 
        if random.random() < 0.5:
            row[desc_col] = desc + " " + random.choice(extras)
    return row
def main(target_rows: int = TARGET_ROWS):
    if not SRC_PATH.exists():
        raise FileNotFoundError(f"Source CSV not found: {SRC_PATH}")
    df = pd.read_csv(SRC_PATH)
    print(f"Loaded {len(df)} rows from {SRC_PATH}")
    if len(df) == 0:
        raise ValueError("sample_jobs.csv is empty, cannot generate synthetic data.")
    title_col = find_col(df, TITLE_COLS)
    company_col = find_col(df, COMPANY_COLS)
    location_col = find_col(df, LOCATION_COLS)
    desc_col = find_col(df, DESC_COLS)
    sal_min_col = find_col(df, SAL_MIN_COLS)
    sal_max_col = find_col(df, SAL_MAX_COLS)
    sal_raw_col = find_col(df, SAL_RAW_COLS)
    print("Using columns:")
    print("  title     :", title_col)
    print("  company   :", company_col)
    print("  location  :", location_col)
    print("  desc      :", desc_col)
    print("  salary_min:", sal_min_col)
    print("  salary_max:", sal_max_col)
    print("  salary_raw:", sal_raw_col)
    repeats = math.ceil(target_rows / len(df))
    frames = []
    for i in range(repeats):
        tmp = df.copy()
        tmp = tmp.apply(
            augment_row,
            axis=1,
            args=(title_col, company_col, location_col,sal_min_col, sal_max_col, sal_raw_col, desc_col),)
        frames.append(tmp)
    big = pd.concat(frames, ignore_index=True)
    big = big.sample(n=target_rows, replace=False, random_state=42)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    big.to_csv(OUT_PATH, index=False)
    print(f"✅ Generated synthetic dataset: {OUT_PATH}")
    print(f"   Total rows: {len(big)}")
if __name__ == "__main__":
    main()