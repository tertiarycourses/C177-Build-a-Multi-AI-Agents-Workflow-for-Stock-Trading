"""Performance Analysis Agent: return and risk metrics of the agent's trading, for the dashboard."""
from __future__ import annotations

import math

from trading_agents import store
from trading_agents.broker import START_CASH, get_broker
from trading_agents.llm import ask_json

NAME = "performance_analysis"
ROLE = "You are the Performance Analysis Agent. Explain the metrics in two sentences for the dashboard."


def metrics(curve: list[float], trades: list[dict]) -> dict:
    rets = [b / a - 1 for a, b in zip(curve, curve[1:]) if a]
    mean = sum(rets) / len(rets) if rets else 0.0
    sd = math.sqrt(sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)) if len(rets) > 1 else 0.0
    peak, mdd = curve[0] if curve else START_CASH, 0.0
    for v in curve:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    closed = [t for t in trades if t.get("side") == "close"]
    wins = sum(1 for t in closed if t.get("realized", 0) > 0)
    return {"total_return_pct": round((curve[-1] / START_CASH - 1) * 100, 3) if curve else 0.0,
            "sharpe": round(mean / sd * math.sqrt(252), 2) if sd else 0.0,
            "max_drawdown_pct": round(mdd * 100, 3),
            "win_rate_pct": round(wins / len(closed) * 100, 1) if closed else 0.0,
            "trades": len(trades)}


def run(broker=None) -> tuple[dict, str]:
    broker = broker or get_broker()
    equity = broker.equity()
    store.append("equity.jsonl", {"equity": equity})
    curve = [r["equity"] for r in store.rows("equity.jsonl")]
    m = {"equity": equity, **metrics([START_CASH] + curve, store.rows("trades.jsonl")),
         "open_positions": broker.positions()}
    out, brain = ask_json(ROLE, m, {**m, "summary": f"Equity {equity:,.2f}, return {m['total_return_pct']}%, "
                                                     f"max drawdown {m['max_drawdown_pct']}%, {m['trades']} trades."},
                          ["summary"])
    store.write("performance.json", out)
    return out, brain
