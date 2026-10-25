"""Lab 8 - Strategy Review, Lead Agent orchestration and the feedback loop."""
from trading_agents import store
from trading_agents.agents import lead, strategy_review

ORDER = ["lead", "finance_research", "news_sentiment", "trading_strategy", "signal_generation", "stock_trader",
         "performance_analysis", "strategy_review"]


def test_lab8_full_workflow_and_feedback_loop():
    run = lead.run(["NVDA", "AAPL", "SPY"])
    agents = [t["agent"] for t in run["trace"]]
    assert agents[0] == "lead" and agents[-1] == "lead" and all(a in agents for a in ORDER)
    assert {"total_return_pct", "sharpe", "max_drawdown_pct", "win_rate_pct"} <= set(run["performance"])
    guidance = store.read("guidance.json", None)
    assert guidance and abs(sum(guidance["weights"].values()) - 1) < 0.01
    again = lead.run(["NVDA"])
    strat = next(t["output"] for t in again["trace"] if t["agent"] == "trading_strategy")
    assert strat["entry_threshold"] == guidance["entry_threshold"]


def test_lab8_review_raises_threshold_after_losses():
    store.write("guidance.json", {"entry_threshold": 0.3})
    out, _ = strategy_review.run({"trades": 4, "total_return_pct": -2.0}, [])
    assert out["verdict"] == "adjust" and out["entry_threshold"] > 0.3
