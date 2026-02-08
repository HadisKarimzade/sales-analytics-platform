from pathlib import Path
import pandas as pd

def ensure_dirs(paths):
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)

def to_datetime_series(s):
    return pd.to_datetime(s, errors="coerce")

def to_numeric_series(s):
    return pd.to_numeric(s, errors="coerce")

def clean_status(x):
    if pd.isna(x):
        return "pending"
    x = str(x).strip().lower()
    return x if x in {"completed", "cancelled", "pending"} else "pending"
