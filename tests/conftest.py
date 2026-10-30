import os
import sys
from pathlib import Path

# Point the app at a throw-away SQLite file *before* src.* is imported.
_DB = Path(__file__).parent / "_test.db"
if _DB.exists():
    _DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{_DB}"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
