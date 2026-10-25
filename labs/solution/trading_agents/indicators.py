"""Technical indicators, computed in code (never by the LLM). Input: OHLCV DataFrame indexed by time."""
from __future__ import annotations

import numpy as np
import pandas as pd


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    down = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / down.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


def macd(close: pd.Series, fast: int = 12, slow: int = 26, sig: int = 9) -> tuple[pd.Series, pd.Series]:
    line = ema(close, fast) - ema(close, slow)
    return line, ema(line, sig)


def vwap(df: pd.DataFrame) -> pd.Series:
    typical = (df["high"] + df["low"] + df["close"]) / 3
    vol = df["volume"].replace(0, np.nan)
    return ((typical * vol).cumsum() / vol.cumsum()).ffill().fillna(df["close"])


def bollinger(close: pd.Series, n: int = 20, k: float = 2.0) -> tuple[pd.Series, pd.Series, pd.Series]:
    mid = close.rolling(n).mean()
    sd = close.rolling(n).std()
    return mid - k * sd, mid, mid + k * sd


def snapshot(df: pd.DataFrame) -> dict:
    """Latest value of every indicator the Trading Strategy Agent votes on."""
    c = df["close"]
    m_line, m_sig = macd(c)
    lo, mid, hi = bollinger(c)
    return {
        "close": round(float(c.iloc[-1]), 4),
        "ema_fast": round(float(ema(c, 20).iloc[-1]), 4),
        "ema_slow": round(float(ema(c, 50).iloc[-1]), 4),
        "momentum_pct": round(float(c.pct_change(10).iloc[-1] * 100), 3),
        "rsi": round(float(rsi(c).iloc[-1]), 2),
        "macd": round(float(m_line.iloc[-1]), 4),
        "macd_signal": round(float(m_sig.iloc[-1]), 4),
        "vwap": round(float(vwap(df).iloc[-1]), 4),
        "bb_low": round(float(lo.iloc[-1]), 4),
        "bb_high": round(float(hi.iloc[-1]), 4),
    }


def votes(ind: dict) -> dict:
    """Each algorithm's vote: +1 long, -1 short, 0 no view."""
    sign = lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
    c = ind["close"]
    vol = 1 if c > ind["bb_high"] else (-1 if c < ind["bb_low"] else 0)   # breakout of the bands
    r = ind["rsi"]
    return {
        "trend": sign(ind["ema_fast"] - ind["ema_slow"]),
        "momentum": sign(ind["momentum_pct"]),
        "volatility": vol,
        "vwap": sign(c - ind["vwap"]),
        "rsi": 1 if r < 30 else (-1 if r > 70 else 0),                      # mean reversion at extremes
        "macd": sign(ind["macd"] - ind["macd_signal"]),
    }
