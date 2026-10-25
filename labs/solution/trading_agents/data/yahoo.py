"""Yahoo Finance company profile and key financial ratios via the yfinance package (no key)."""
from __future__ import annotations

from trading_agents.config import settings
from trading_agents.data import sample

FIELDS = ("shortName", "sector", "industry", "marketCap", "trailingPE", "forwardPE", "priceToBook", "profitMargins",
          "revenueGrowth", "earningsGrowth", "debtToEquity", "returnOnEquity", "beta", "fiftyTwoWeekHigh",
          "fiftyTwoWeekLow", "recommendationKey")


def company(symbol: str) -> dict:
    if settings().offline:
        return sample.load("yahoo_company", symbol)
    import yfinance as yf
    info = yf.Ticker(symbol).info or {}
    return {k: info.get(k) for k in FIELDS}
