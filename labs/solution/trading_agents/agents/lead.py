"""Lead Agent: orchestrates the whole flow and writes the run summary.

Lead -> [Finance Research || News Sentiment] -> Trading Strategy -> Signal Generation -> Stock Trader
     -> Performance Analysis -> Strategy Review -> (guidance feeds Trading Strategy next run) -> Lead summary
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor

from trading_agents import store
from trading_agents.agents import (finance_research, news_sentiment, performance_analysis, signal_generation,
                                   stock_trader, strategy_review, trading_strategy)
from trading_agents.broker import get_broker
from trading_agents.llm import ask_json

NAME = "lead"
ROLE = "You are the Lead Agent. Summarise this run for the trader in three sentences: signals, orders and what changes next."


def _step(trace: list, agent: str, fn, *args):
    t0 = time.time()
    out, brain = fn(*args)
    trace.append({"agent": agent, "brain": brain, "ms": int((time.time() - t0) * 1000), "output": out})
    return out


def run(symbols: list[str]) -> dict:
    trace: list[dict] = [{"agent": NAME, "brain": "code", "ms": 0,
                          "output": {"plan": ["research+sentiment (parallel)", "strategy", "signal", "trade",
                                              "performance", "review"], "symbols": symbols}}]
    broker = get_broker()
    guidance = store.read("guidance.json", None)
    strategies, signals, orders = [], [], []
    for sym in [s.upper() for s in symbols]:
        with ThreadPoolExecutor(max_workers=2) as pool:            # the two research agents run in parallel
            f_fin = pool.submit(finance_research.run, sym)
            f_sen = pool.submit(news_sentiment.run, sym)
            (fin, fb), (sen, sb) = f_fin.result(), f_sen.result()
        trace += [{"agent": finance_research.NAME, "brain": fb, "ms": 0, "output": fin},
                  {"agent": news_sentiment.NAME, "brain": sb, "ms": 0, "output": sen}]
        strat = _step(trace, trading_strategy.NAME, trading_strategy.run, fin, sen, guidance)
        sig = _step(trace, signal_generation.NAME, signal_generation.run, strat)
        order = _step(trace, stock_trader.NAME, stock_trader.run, sig, fin["last_price"], broker)
        strategies.append(strat), signals.append(sig), orders.append(order)
    perf = _step(trace, performance_analysis.NAME, performance_analysis.run, broker)
    review = _step(trace, strategy_review.NAME, strategy_review.run, perf, strategies)
    fallback = {"summary": "; ".join(f"{s['symbol']} {s['signal']}" for s in signals)
                + f". Orders: {sum(o['status'] in ('filled', 'submitted') for o in orders)}. "
                f"Review: {review['verdict']}, next threshold {review['entry_threshold']}."}
    summ, brain = ask_json(ROLE, {"signals": signals, "orders": orders, "performance": perf, "review": review},
                           fallback, ["summary"])
    trace.append({"agent": NAME, "brain": brain, "ms": 0, "output": summ})
    run = {"symbols": symbols, "signals": signals, "orders": orders, "performance": perf, "review": review,
           "summary": summ["summary"], "trace": trace}
    store.append("runs.jsonl", {k: run[k] for k in ("symbols", "signals", "orders", "summary")})
    return run
