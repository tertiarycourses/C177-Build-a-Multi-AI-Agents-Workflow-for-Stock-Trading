"""Equibles REST API: valuation multiples, short interest and insider transactions (Bearer key)."""
from __future__ import annotations

import httpx

from trading_agents.config import settings
from trading_agents.data import sample

URL = "https://api.equibles.com/v1"


def _get(path: str, params: dict | None = None) -> dict:
    r = httpx.get(f"{URL}{path}", params=params or {},
                  headers={"Authorization": f"Bearer {settings().equibles_key}"}, timeout=30)
    r.raise_for_status()
    return r.json()


def company(symbol: str) -> dict:
    s = settings()
    if s.offline or not s.equibles_key:
        return sample.load("equibles", symbol)
    sym = symbol.upper()
    out: dict = {"errors": {}}
    for key, path, params in (("valuation", f"/stocks/{sym}/valuation-multiples", None),
                              ("short_interest", f"/stocks/{sym}/short-interest", {"limit": 3}),
                              ("insider", f"/stocks/{sym}/insider-transactions", {"limit": 10})):
        try:
            js = _get(path, params)
            out[key] = js.get("data", js) if key != "valuation" else js
        except Exception as exc:                  # an ETF has no P/E: record and continue
            out[key], out["errors"][key] = None, str(exc)[:160]
    return out
