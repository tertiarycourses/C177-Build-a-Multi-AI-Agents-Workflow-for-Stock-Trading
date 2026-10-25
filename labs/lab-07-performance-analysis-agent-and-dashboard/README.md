# Lab 7 - Build the Performance Analysis Agent and the Dashboard

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 03:** Execution, Performance and the Feedback Loop  |  **Time:** 30 min

**Learning outcome:** LO4: vibe-code an agent that computes return and risk metrics and a dashboard that shows them.

Build the agent that records the equity after every run and computes total return, Sharpe ratio, maximum drawdown, win rate and trade count, then a Streamlit dashboard that runs the workflow and shows the metrics, the equity curve, the signals and the orders.

## Key concepts

- **Total return** - Latest equity / starting equity - 1.
- **Sharpe ratio** - Mean of per-run returns / their standard deviation x sqrt(252).
- **Maximum drawdown** - The worst fall from a running equity peak.
- **Win rate** - Share of closing trades with positive realised P&L.

## What you'll build

agents/performance_analysis.py (metrics() and run()) and dashboard.py

**Tools:** Streamlit, pandas, Claude Code or Codex

## Steps

1. **Prompt for the agent.**
   Paste into your AI coding assistant:

   ```text
   Create agents/performance_analysis.py, NAME='performance_analysis', metrics(curve, trades) returning total_return_pct, sharpe, max_drawdown_pct, win_rate_pct and trades, and run(broker=None) that appends the equity to equity.jsonl, computes the metrics from the equity curve and trades.jsonl, adds open positions, lets ask_json() write a two-sentence summary, and saves performance.json.
   ```

2. **Prompt for the dashboard.**
   Paste into your AI coding assistant:

   ```text
   Create dashboard.py in Streamlit: a symbols box and a 'Run the workflow' button, a five-metric row (equity, return, Sharpe, max drawdown, win rate) from performance.json, a line chart of equity.jsonl, and the strategy guidance from guidance.json.
   ```

3. **Run the check and open the dashboard.**

   ```bash
   pytest -q tests/test_lab7.py
   streamlit run dashboard.py
   ```

4. **Commit.**

   ```bash
   git add -A && git commit -m "Lab 7: performance analysis agent and dashboard"
   ```

## Verify

tests/test_lab7.py passes: a rising equity curve gives a positive return and zero drawdown; a fall gives a negative drawdown. The dashboard shows the five metrics after a run.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
