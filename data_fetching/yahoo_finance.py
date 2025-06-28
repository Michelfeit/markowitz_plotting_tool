from __future__ import annotations
import datetime as dt
import os

from data_fetching.data_management import _folder_name, _data_path, check_cache, save_to_disk
import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path

def get_means_and_cov(
    tickers: list[str],
    start: str,
    end: str | None = None,
    interval: str = "1d",
    annualise=True,
    force_refresh=False
) -> tuple[np.ndarray, pd.DataFrame]:
    """
    Returns (meanVector, covMatrix) – either from disk or from Yahoo Finance.
    """
    if end is None:
        end = dt.date.today().strftime("%Y-%m-%d")

    folder = os.path.join(Path(_data_path()),Path(_folder_name(start, end)))

    if not force_refresh:
        exists, mean, cov = check_cache(start, end, tickers)
        if exists: return mean, cov
    # ---------------- fetch & compute ----------------
    prices = (yf.download(tickers, start=start, end=end,
                          interval=interval, auto_adjust=True)
              .loc[:, "Close"].ffill().dropna(how="all"))
    rets = prices.pct_change().dropna()
    mean = rets.mean()

    cov  = rets.cov()
    if annualise:
        scaler = {"1d": 252, "1wk": 52, "1mo": 12}.get(interval, 1)
        mean *= scaler
        cov  *= scaler

    save_to_disk(mean, cov, start, end, tickers, interval)

    return mean, cov