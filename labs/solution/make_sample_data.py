"""Regenerate the synthetic offline sample data (training only - not real prices)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "sample_data"
SPECS = {"NVDA": (180.0, 0.0009), "AAPL": (230.0, -0.0004), "SPY": (580.0, 0.0002)}
FREQ = {"1min": "1min", "15min": "15min", "1h": "1h"}


def series(price: float, drift: float, n: int, freq: str, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rets = rng.normal(drift, 0.004, n)
    close = price * np.exp(np.cumsum(rets))
    idx = pd.date_range("2026-10-19 09:30", periods=n, freq=freq)
    open_ = np.r_[price, close[:-1]]
    high = np.maximum(open_, close) * (1 + rng.uniform(0, 0.002, n))
    low = np.minimum(open_, close) * (1 - rng.uniform(0, 0.002, n))
    vol = rng.integers(20_000, 200_000, n)
    return pd.DataFrame({"timestamp": idx, "open": open_, "high": high, "low": low, "close": close, "volume": vol})


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for i, (sym, (p, d)) in enumerate(SPECS.items()):
        for j, (iv, f) in enumerate(FREQ.items()):
            series(p, d, 300, f, 100 * i + j).round({"open": 4, "high": 4, "low": 4, "close": 4}).to_csv(OUT / f"{sym}_{iv}.csv", index=False)
    print("written to", OUT)
