"""Lab 1 - project scaffold, message contract, LLM fallback."""
from trading_agents import messages
from trading_agents.llm import ask_json


def test_lab1_contract_and_llm_fallback():
    for name in ("FinanceReport", "SentimentReport", "Strategy", "TradeSignal", "OrderResult", "Performance", "Review"):
        assert hasattr(messages, name)
    assert set(messages.ALGORITHMS) == {"trend", "momentum", "volatility", "vwap", "rsi", "macd"}
    out, brain = ask_json("test", {"x": 1}, {"summary": "fallback"}, ["summary"])
    assert out["summary"] == "fallback" and brain == "rules"
