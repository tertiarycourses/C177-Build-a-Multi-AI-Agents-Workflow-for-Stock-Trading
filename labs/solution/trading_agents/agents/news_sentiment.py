"""News Sentiment Agent: Reddit posts + NewsAPI headlines -> sentiment score -1..1."""
from __future__ import annotations

from trading_agents import sentiment
from trading_agents.data import newsapi, reddit
from trading_agents.llm import ask_json

NAME = "news_sentiment"
ROLE = ("You are the News Sentiment Agent. Judge the overall sentiment for the stock from the Reddit posts and "
        "news headlines on a scale of -1 (very negative) to +1 (very positive). Flag event risk.")


def run(symbol: str) -> tuple[dict, str]:
    posts = reddit.posts(symbol)
    news = newsapi.headlines(symbol)
    r_texts = [f"{p['title']} {p.get('text', '')}" for p in posts]
    n_texts = [f"{a['title']} {a.get('description', '')}" for a in news]
    r_score, n_score = sentiment.average(r_texts), sentiment.average(n_texts)
    combined = round(0.4 * r_score + 0.6 * n_score, 3)        # news weighted above social chatter
    fallback = {
        "symbol": symbol, "score": combined,
        "reddit": {"posts": len(posts), "score": r_score, "top": [p["title"] for p in posts[:3]]},
        "news": {"articles": len(news), "score": n_score, "top": [a["title"] for a in news[:3]]},
        "summary": f"Reddit {r_score:+.2f} over {len(posts)} posts, news {n_score:+.2f} over {len(news)} headlines.",
    }
    out, brain = ask_json(ROLE, {"symbol": symbol, "reddit": r_texts[:25], "news": n_texts[:25],
                                 "lexicon_score": combined}, fallback, ["score", "summary"])
    out["score"] = max(-1.0, min(1.0, float(out.get("score", combined))))
    return out, brain
