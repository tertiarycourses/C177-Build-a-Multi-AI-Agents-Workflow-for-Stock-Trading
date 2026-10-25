"""Lab 2 - Finance Research Agent."""
from trading_agents.agents import finance_research


def test_lab2_finance_research_uses_three_intervals():
    out, _ = finance_research.run("NVDA")
    assert set(out["candles"]) == {"1min", "15min", "1h"}
    assert out["last_price"] > 0 and "rsi" in out["indicators"] and out["company"] and out["equibles"]
