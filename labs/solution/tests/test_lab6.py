"""Lab 6 - Stock Trader Agent (offline paper simulator)."""
from trading_agents.agents import stock_trader
from trading_agents.broker import PaperSim


def test_lab6_trader_long_short_null_and_flip():
    b = PaperSim()
    o, _ = stock_trader.run({"symbol": "NVDA", "signal": "long"}, 100.0, b)
    assert o["status"] == "filled" and b.position("NVDA") > 0
    stock_trader.run({"symbol": "NVDA", "signal": "short"}, 100.0, b)
    assert b.position("NVDA") < 0
    o, _ = stock_trader.run({"symbol": "NVDA", "signal": "null"}, 100.0, b)
    assert o["action"] == "none"
