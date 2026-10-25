"""Stock Trader Agent: places the order on the Alpaca PAPER account (or the offline simulator).

long  -> hold +N shares (buy, closing any short first)
short -> hold -N shares (sell short, closing any long first)
null  -> no order
"""
from __future__ import annotations

from trading_agents import store
from trading_agents.broker import get_broker
from trading_agents.config import settings

NAME = "stock_trader"


def run(signal: dict, price: float, broker=None) -> tuple[dict, str]:
    broker = broker or get_broker()
    sym = signal["symbol"]
    broker.mark(sym, price)
    held = broker.position(sym)
    if signal["signal"] == "null":
        return {"symbol": sym, "signal": "null", "action": "none", "qty": 0, "price": price, "broker": broker.name,
                "status": "skipped", "detail": "null signal - no order"}, "code"
    target_dir = 1 if signal["signal"] == "long" else -1
    if held and (held > 0) == (target_dir > 0):
        return {"symbol": sym, "signal": signal["signal"], "action": "none", "qty": 0, "price": price,
                "broker": broker.name, "status": "skipped", "detail": f"already {signal['signal']} {abs(held)}"}, "code"
    size = int(broker.equity() * settings().position_pct // price) if price > 0 else 0
    results = []
    try:
        if held:                                                     # flip: close the opposite position first
            r = broker.submit(sym, "buy" if held < 0 else "sell", abs(held), price)
            results.append(r)
            store.append("trades.jsonl", {"symbol": sym, "side": "close", "qty": abs(held), "price": price,
                                          "realized": r.get("realized", 0.0)})
        if size > 0:
            side = "buy" if target_dir > 0 else "sell"
            r = broker.submit(sym, side, size, price)
            results.append(r)
            store.append("trades.jsonl", {"symbol": sym, "side": side, "qty": size, "price": price, "realized": 0.0})
        status = results[-1]["status"] if results else "skipped"
        detail = "; ".join(r["detail"] for r in results) or "size rounds to zero shares"
    except Exception as exc:                       # e.g. a stock Alpaca cannot short
        status, detail = "error", f"{type(exc).__name__}: {str(exc)[:200]}"
    action = "buy" if target_dir > 0 else "sell_short"
    return {"symbol": sym, "signal": signal["signal"], "action": action, "qty": size, "price": price,
            "broker": broker.name, "status": status, "detail": detail}, "code"
