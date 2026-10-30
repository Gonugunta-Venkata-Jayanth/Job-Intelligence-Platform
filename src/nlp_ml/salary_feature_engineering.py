"""Feature construction shared by salary-model training and inference.

The model is a TF-IDF + RandomForest pipeline over a single text field built
from the job title, description and raw location. Keeping this in one place
guarantees training and inference build exactly the same input.
"""
import pandas as pd

TEXT_COLUMNS = ("title", "description", "raw_location")


def combine_text(row) -> str:
    return " \n".join(str(row.get(col) or "") for col in TEXT_COLUMNS)


def add_text_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add a ``text`` column (title + description + location) to ``df``."""
    if not df.empty:
        df["text"] = df.apply(combine_text, axis=1)
    else:
        df["text"] = pd.Series(dtype=str)
    return df


def add_avg_salary_target(df: pd.DataFrame) -> pd.DataFrame:
    """Add the training target ``avg_salary`` = mean of min and max salary."""
    df["min_salary"] = df["min_salary"].astype(float)
    df["max_salary"] = df["max_salary"].astype(float)
    df["avg_salary"] = (df["min_salary"] + df["max_salary"]) / 2.0
    return df
