"""Trading Strategy Agent: merge finance + sentiment, pick an algorithm or a mix, score the setup."""
from __future__ import annotations

from trading_agents import indicators
from trading_agents.llm import ask_json
from trading_agents.messages import ALGORITHMS

NAME = "trading_strategy"
ROLE = ("You are the Trading Strategy Agent. Choose one algorithm or a weighted mix from: "
        + ", ".join(ALGORITHMS) + ". Use the computed votes, the sentiment and the strategy-review guidance. "
        "Weights must sum to 1.")

DEFAULT_GUIDANCE = {"preferred_algorithms": ["trend", "macd", "rsi"], "weights": {"trend": 0.4, "macd": 0.35,
                    "rsi": 0.25}, "entry_threshold": 0.3, "sentiment_weight": 0.3}


def run(finance: dict, sentiment: dict, guidance: dict | None) -> tuple[dict, str]:
    g = {**DEFAULT_GUIDANCE, **(guidance or {})}
    votes = indicators.votes(finance["indicators"])               # computed in code, never by the LLM
    fallback_weights = {a: w for a, w in g["weights"].items() if a in ALGORITHMS} or {"trend": 1.0}
    out, brain = ask_json(ROLE, {"votes": votes, "finance": finance["summary"], "sentiment": sentiment["score"],
                                 "guidance": g},
                          {"algorithms": list(fallback_weights), "weights": fallback_weights,
                           "rationale": f"Guidance mix {fallback_weights} with sentiment weight {g['sentiment_weight']}."},
                          ["algorithms", "weights", "rationale"])
    w = {a: float(v) for a, v in (out.get("weights") or {}).items() if a in ALGORITHMS and float(v) > 0}
    w = w or fallback_weights
    total = sum(w.values())
    w = {a: round(v / total, 3) for a, v in w.items()}
    tech = sum(w[a] * votes[a] for a in w)
    sw = float(g["sentiment_weight"])
    combined = round((1 - sw) * tech + sw * float(sentiment["score"]), 3)
    return {"symbol": finance["symbol"], "algorithms": list(w), "weights": w, "votes": votes,
            "sentiment_weight": sw, "combined_score": combined, "entry_threshold": g["entry_threshold"],
            "rationale": out.get("rationale", "")}, brain
