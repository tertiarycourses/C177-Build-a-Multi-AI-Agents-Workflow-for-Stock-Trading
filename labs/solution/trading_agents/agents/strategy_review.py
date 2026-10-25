"""Strategy Review Agent: reviews performance and recent signals, updates the guidance the strategy agent reads."""
from __future__ import annotations

from trading_agents import store
from trading_agents.agents.trading_strategy import DEFAULT_GUIDANCE
from trading_agents.llm import ask_json
from trading_agents.messages import ALGORITHMS

NAME = "strategy_review"
ROLE = ("You are the Strategy Review Agent. Review the performance and the recent strategies and signals. "
        "Keep or adjust the algorithm mix, weights and entry threshold for the next run, and explain why.")


def run(performance: dict, strategies: list[dict]) -> tuple[dict, str]:
    old = {**DEFAULT_GUIDANCE, **store.read("guidance.json", {})}
    weights = dict(old["weights"])
    notes = []
    verdict = "keep"
    if performance["trades"] >= 2 and performance["total_return_pct"] < 0:
        # rule brain: shift weight toward the algorithms that agreed with the outcome, raise the bar
        verdict = "adjust"
        old["entry_threshold"] = round(min(0.6, old["entry_threshold"] + 0.05), 2)
        notes.append("negative return - raised the entry threshold by 0.05")
    agree: dict[str, int] = {}
    for s in strategies:
        for algo, vote in s["votes"].items():
            agree[algo] = agree.get(algo, 0) + (1 if vote and (vote > 0) == (s["combined_score"] > 0) else 0)
    fallback = {"verdict": verdict, "preferred_algorithms": list(weights), "weights": weights,
                "entry_threshold": old["entry_threshold"], "sentiment_weight": old["sentiment_weight"],
                "notes": notes or ["performance within expectations - keep the current mix"]}
    out, brain = ask_json(ROLE, {"performance": performance, "strategies": strategies, "current": old,
                                 "algorithm_agreement": agree}, fallback,
                          ["verdict", "preferred_algorithms", "weights", "entry_threshold", "notes"])
    w = {a: float(v) for a, v in (out.get("weights") or {}).items() if a in ALGORITHMS and float(v) > 0} or weights
    total = sum(w.values())
    out["weights"] = {a: round(v / total, 3) for a, v in w.items()}
    out["preferred_algorithms"] = list(out["weights"])
    out["entry_threshold"] = max(0.05, min(0.9, float(out.get("entry_threshold", old["entry_threshold"]))))
    store.write("guidance.json", {k: out[k] for k in ("preferred_algorithms", "weights", "entry_threshold",
                                                      "sentiment_weight", "notes", "verdict")})
    return out, brain
