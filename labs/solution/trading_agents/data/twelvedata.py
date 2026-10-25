"""Twelve Data time series: 1min, 15min and 1h candles for the Finance Research Agent."""
from __future__ import annotations

import httpx
import pandas as pd

from trading_agents.config import settings
from trading_agents.data import sample

URL = "https://api.twelvedata.com/time_series"
INTERVALS = ("1min", "15min", "1h")


def candles(symbol: str, interval: str, outputsize: int = 300) -> pd.DataFrame:
    s = settings()
    if s.offline or not s.twelvedata_key:
        return sample.candles(symbol, interval)
    r = httpx.get(URL, params={"symbol": symbol, "interval": interval, "outputsize": outputsize, "order": "asc",
                               "timezone": "America/New_York"},
                  headers={"Authorization": f"apikey {s.twelvedata_key}"}, timeout=30)
    js = r.json()
    if js.get("status") != "ok":
        raise RuntimeError(f"Twelve Data error: {js.get('message', js)}")
    df = pd.DataFrame(js["values"])
    df["timestamp"] = pd.to_datetime(df["datetime"])
    if "volume" not in df:
        df["volume"] = 0
    return df.set_index("timestamp")[["open", "high", "low", "close", "volume"]].astype(float).sort_index()
