"""NewsAPI.org /v2/everything: recent headlines about a symbol."""
from __future__ import annotations

import httpx

from trading_agents.config import settings
from trading_agents.data import sample


def headlines(symbol: str, query: str | None = None, page_size: int = 30) -> list[dict]:
    s = settings()
    if s.offline or not s.newsapi_key:
        return sample.load("news", symbol)
    r = httpx.get("https://newsapi.org/v2/everything", headers={"X-Api-Key": s.newsapi_key}, timeout=20,
                  params={"q": query or symbol, "language": "en", "sortBy": "publishedAt", "pageSize": page_size})
    js = r.json()
    if js.get("status") != "ok":
        raise RuntimeError(f"NewsAPI error: {js.get('code')}: {js.get('message')}")
    return [{"title": a.get("title") or "", "description": a.get("description") or "",
             "source": (a.get("source") or {}).get("name", ""), "url": a.get("url", ""),
             "published": a.get("publishedAt", "")} for a in js.get("articles", [])]
