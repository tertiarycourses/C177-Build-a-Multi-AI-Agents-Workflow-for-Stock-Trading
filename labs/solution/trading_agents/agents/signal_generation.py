"""Signal Generation Agent: strategy -> long, short or null."""
from __future__ import annotations

from trading_agents.llm import ask_json

NAME = "signal_generation"
ROLE = ("You are the Signal Generation Agent. Turn the strategy's combined score into exactly one signal: "
        "long, short or null, with a confidence from 0 to 1.")


def rule_signal(score: float, threshold: float) -> str:
    return "long" if score >= threshold else ("short" if score <= -threshold else "null")


def run(strategy: dict) -> tuple[dict, str]:
    sig = rule_signal(strategy["combined_score"], strategy["entry_threshold"])
    fallback = {"symbol": strategy["symbol"], "signal": sig,
                "confidence": round(min(1.0, abs(strategy["combined_score"])), 2),
                "rationale": f"combined score {strategy['combined_score']:+.2f} vs threshold "
                             f"+/-{strategy['entry_threshold']}"}
    out, brain = ask_json(ROLE, strategy, fallback, ["signal", "confidence", "rationale"])
    if out.get("signal") not in ("long", "short", "null"):
        out["signal"] = sig
    out["confidence"] = max(0.0, min(1.0, float(out.get("confidence", 0))))
    return out, brain
