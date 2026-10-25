"""Lab 7 - Performance Analysis Agent."""
from trading_agents.agents.performance_analysis import metrics


def test_lab7_performance_metrics():
    up = metrics([100_000, 101_000, 102_000], [])
    assert up["total_return_pct"] > 0 and up["max_drawdown_pct"] == 0
    down = metrics([100_000, 104_000, 98_000], [{"side": "close", "realized": 50}, {"side": "close", "realized": -20}])
    assert down["max_drawdown_pct"] < 0 and down["win_rate_pct"] == 50.0
