from __future__ import annotations
import json, datetime as dt
from pathlib import Path
from typing import Any

import pandas as pd

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, Path("../data_cache/csv"))
CATALOGUE = os.path.join(DATA_DIR, Path("catalogue.json"))
Path(DATA_DIR).mkdir(exist_ok=True)

def _data_path():
    return DATA_DIR

def _load_catalogue() -> dict:
    if Path(CATALOGUE).exists():
        return json.loads(Path(CATALOGUE).read_text())
    return {}

def _store_catalogue(cat: dict) -> None:
    CATALOGUE.write_text(json.dumps(cat, indent=2, default=str))

def _folder_name(start: str, end: str) -> str:
    return f"{start}_{end}"

def log_dataframe(df):
    name = "dax_may_2025.csv"
    dir = Path("data_cache/csv") / name
    df.to_csv(dir, header=True)

def check_cache(start, end, tickers):
    folder = os.path.join(Path(_data_path()),Path(_folder_name(start, end)))
    catalogue = _load_catalogue()
    cached = Path(folder).name in catalogue
    mean_dir = os.path.join(folder, "mean.csv")
    cov_dir = os.path.join(folder, "covariance.csv")
    key = f"{start}_{end}"
    # Load catalog
    """"""
    with open(CATALOGUE, 'r') as f:
        catalog = json.load(f)
    # Check if key exists
    if key not in catalog:
        return False, None, None
    # Compare sorted ticker lists (ignoring order)
    catalog_tickers = catalog[key]["tickers"]
    if not set(tickers).issubset(set(catalog_tickers)):
        return False, None, None
    if not cached:
        return False, None, None
    mean = pd.read_csv(mean_dir, index_col=0).squeeze("columns")
    cov = pd.read_csv(cov_dir, index_col=0).squeeze("columns")
    return True, mean, cov


def save_to_disk(mean, cov, start, end, ticker, interval):
    # ---------------- save to disk -------------------
    folder = _data_path() / _folder_name(start, end)
    mean_dir = folder / "mean.csv"
    cov_dir = folder / "covariance.csv"
    catalogue = _load_catalogue()

    folder.mkdir(exist_ok=True)
    mean.to_csv(mean_dir, header=True)
    cov.to_csv(cov_dir, header=True)

    # update catalogue
    catalogue[folder.name] = {
        "tickers": ticker,
        "interval": interval,
        "created": dt.datetime.now().isoformat(timespec="seconds")
    }
    _store_catalogue(catalogue)

def get_dax_df():
    name = "dax_may_2025.csv"
    dir = DATA_DIR / name
    return pd.read_csv(dir, index_col=0).squeeze("columns")