"""Reddit API (OAuth application-only flow): recent posts mentioning a symbol in finance subreddits.

Create a "script" app at https://www.reddit.com/prefs/apps, then set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
and a descriptive REDDIT_USER_AGENT. Reddit requires the User-Agent on every request.
"""
from __future__ import annotations

import httpx

from trading_agents.config import settings
from trading_agents.data import sample

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API = "https://oauth.reddit.com"


def token() -> str:
    s = settings()
    r = httpx.post(TOKEN_URL, data={"grant_type": "client_credentials"}, auth=(s.reddit_id, s.reddit_secret),
                   headers={"User-Agent": s.reddit_agent}, timeout=20)
    r.raise_for_status()
    return r.json()["access_token"]


def posts(symbol: str, limit: int = 25) -> list[dict]:
    s = settings()
    if s.offline or not (s.reddit_id and s.reddit_secret):
        return sample.load("reddit", symbol)
    headers = {"Authorization": f"bearer {token()}", "User-Agent": s.reddit_agent}
    out: list[dict] = []
    for sub in [x.strip() for x in s.reddit_subs.split(",") if x.strip()]:
        r = httpx.get(f"{API}/r/{sub}/search", headers=headers, timeout=20,
                      params={"q": symbol, "restrict_sr": 1, "sort": "new", "t": "week", "limit": limit})
        r.raise_for_status()
        for child in r.json().get("data", {}).get("children", []):
            d = child.get("data", {})
            out.append({"subreddit": sub, "title": d.get("title", ""), "text": (d.get("selftext") or "")[:500],
                        "score": d.get("score", 0), "comments": d.get("num_comments", 0),
                        "url": "https://www.reddit.com" + d.get("permalink", "")})
    return out
