"""Run the multi AI agents workflow once:  python run.py NVDA AAPL SPY"""
from __future__ import annotations

import json
import sys

from trading_agents.agents import lead

if __name__ == "__main__":
    symbols = sys.argv[1:] or ["NVDA", "AAPL", "SPY"]
    result = lead.run(symbols)
    for step in result["trace"]:
        print(f"[{step['agent']:<20}] brain={step['brain']}")
    print(json.dumps({"signals": result["signals"], "orders": result["orders"],
                      "performance": result["performance"], "review": result["review"]}, indent=2, default=str))
    print("\nLead summary:", result["summary"])
