"""The message contract: what each agent hands to the next. Every agent returns one of these as a dict."""
from __future__ import annotations

from typing import Literal, TypedDict

Signal = Literal["long", "short", "null"]
ALGORITHMS = ("trend", "momentum", "volatility", "vwap", "rsi", "macd")


class FinanceReport(TypedDict):
    symbol: str
    last_price: float
    candles: dict            # interval -> {"bars": int, "change_pct": float, "last": float}
    indicators: dict         # computed in code on the 15min candles
    company: dict            # Yahoo Finance profile + key ratios
    equibles: dict           # valuation / short interest / insider summary
    summary: str
    sources: list[str]


class SentimentReport(TypedDict):
    symbol: str
    score: float             # -1 (very negative) .. +1 (very positive)
    reddit: dict             # {"posts": int, "score": float, "top": [titles]}
    news: dict               # {"articles": int, "score": float, "top": [titles]}
    summary: str


class Strategy(TypedDict):
    symbol: str
    algorithms: list[str]    # subset of ALGORITHMS
    weights: dict            # algorithm -> weight, sums to 1
    votes: dict              # algorithm -> -1 | 0 | +1, computed in code
    sentiment_weight: float
    combined_score: float    # -1 .. +1
    rationale: str


class TradeSignal(TypedDict):
    symbol: str
    signal: Signal
    confidence: float        # 0 .. 1
    rationale: str


class OrderResult(TypedDict):
    symbol: str
    signal: Signal
    action: str              # buy | sell_short | close | none
    qty: int
    price: float
    broker: str              # alpaca-paper | paper-sim
    status: str              # filled | submitted | skipped | error
    detail: str


class Performance(TypedDict):
    equity: float
    total_return_pct: float
    sharpe: float
    max_drawdown_pct: float
    win_rate_pct: float
    trades: int
    open_positions: dict


class Review(TypedDict):
    verdict: str             # keep | adjust
    preferred_algorithms: list[str]
    weights: dict
    entry_threshold: float   # |combined_score| needed for a long/short signal
    notes: list[str]
