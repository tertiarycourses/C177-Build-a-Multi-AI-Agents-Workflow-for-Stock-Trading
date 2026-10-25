"""Finance Research Agent: Twelve Data candles (1min / 15min / 1h) + Yahoo Finance + Equibles."""
from __future__ import annotations

from trading_agents import indicators
from trading_agents.data import equibles, twelvedata, yahoo
from trading_agents.llm import ask_json

NAME = "finance_research"
ROLE = ("You are the Finance Research Agent on a paper-trading desk. From the candle statistics, indicators, "
        "company profile and Equibles data, write a concise finance summary for the strategy agent.")


def run(symbol: str) -> tuple[dict, str]:
    candles, frames = {}, {}
    for iv in twelvedata.INTERVALS:
        df = twelvedata.candles(symbol, iv)
        frames[iv] = df
        first, last = float(df["close"].iloc[0]), float(df["close"].iloc[-1])
        candles[iv] = {"bars": len(df), "last": round(last, 2), "change_pct": round((last / first - 1) * 100, 2)}
    ind = indicators.snapshot(frames["15min"])
    company = yahoo.company(symbol)
    eq = equibles.company(symbol)
    trend = "up" if ind["ema_fast"] > ind["ema_slow"] else "down"
    fallback = {
        "symbol": symbol, "last_price": candles["1min"]["last"], "candles": candles, "indicators": ind,
        "company": company, "equibles": eq,
        "summary": (f"{symbol} last {candles['1min']['last']}; 15-min trend {trend}, RSI {ind['rsi']}, "
                    f"1h change {candles['1h']['change_pct']}%. P/E {company.get('trailingPE')}, "
                    f"sector {company.get('sector')}."),
        "sources": ["twelvedata:1min,15min,1h", "yahoo-finance", "equibles"],
    }
    out, brain = ask_json(ROLE, {k: fallback[k] for k in ("symbol", "candles", "indicators", "company")},
                          fallback, ["summary"])
    return out, brain
