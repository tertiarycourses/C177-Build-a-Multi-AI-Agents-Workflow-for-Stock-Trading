"""Lab 5 - Signal Generation Agent."""
from trading_agents.agents import signal_generation


def test_lab5_signal_thresholds():
    assert signal_generation.rule_signal(0.5, 0.3) == "long"
    assert signal_generation.rule_signal(-0.5, 0.3) == "short"
    assert signal_generation.rule_signal(0.1, 0.3) == "null"
    out, _ = signal_generation.run({"symbol": "NVDA", "combined_score": 0.45, "entry_threshold": 0.3})
    assert out["signal"] in ("long", "short", "null") and 0 <= out["confidence"] <= 1
