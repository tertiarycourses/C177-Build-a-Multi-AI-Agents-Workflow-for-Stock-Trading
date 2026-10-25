"""A small finance lexicon scorer: the deterministic base the News Sentiment Agent refines with the LLM."""
from __future__ import annotations

import re

POS = {"beat", "beats", "surge", "surges", "rally", "record", "upgrade", "upgraded", "strong", "growth", "bullish",
       "buy", "outperform", "raises", "raised", "profit", "gain", "gains", "soar", "soars", "moon", "calls", "win"}
NEG = {"miss", "misses", "plunge", "plunges", "drop", "drops", "downgrade", "downgraded", "weak", "lawsuit", "probe",
       "bearish", "sell", "underperform", "cuts", "cut", "loss", "losses", "fall", "falls", "crash", "puts", "recall",
       "fraud", "layoffs"}


def score(text: str) -> float:
    words = re.findall(r"[a-z]+", text.lower())
    p = sum(w in POS for w in words)
    n = sum(w in NEG for w in words)
    return 0.0 if p + n == 0 else round((p - n) / (p + n), 3)


def average(texts: list[str]) -> float:
    vals = [score(t) for t in texts]
    return round(sum(vals) / len(vals), 3) if vals else 0.0
