"""Offline sample data (synthetic, for training only) so every lab runs without API keys."""
from __future__ import annotations

import json

import pandas as pd

from trading_agents.config import settings


def candles(symbol: str, interval: str) -> pd.DataFrame:
    path = settings().sample_dir / f"{symbol.upper()}_{interval}.csv"
    if not path.exists():
        path = settings().sample_dir / f"NVDA_{interval}.csv"
    return pd.read_csv(path, parse_dates=["timestamp"], index_col="timestamp")


def load(name: str, symbol: str) -> dict | list:
    data = json.loads((settings().sample_dir / f"{name}.json").read_text())
    return data.get(symbol.upper()) or data.get("NVDA")
