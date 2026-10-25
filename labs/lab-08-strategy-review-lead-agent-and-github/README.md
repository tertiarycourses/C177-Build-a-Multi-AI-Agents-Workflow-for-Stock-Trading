# Lab 8 - Close the Loop: Strategy Review, Lead Agent and GitHub

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 03:** Execution, Performance and the Feedback Loop  |  **Time:** 65 min

**Learning outcome:** LO4: vibe-code the strategy review feedback loop and the lead agent, then publish the project to GitHub.

Build the Strategy Review Agent that reads the performance and rewrites the strategy guidance, and the Lead Agent that orchestrates the whole workflow - the two research agents in parallel, then strategy, signal, trade, performance and review - and summarises the run. Run it twice to watch the loop change the strategy, then push your project to your own GitHub repository.

## Key concepts

- **Review rules** - With two or more trades and a negative return, raise the entry threshold by 0.05 and adjust; otherwise keep. The LLM may re-weight the algorithms.
- **guidance.json** - The review writes it; the strategy agent reads it on the next run - that is the feedback loop.
- **Lead orchestration** - Plan -> [finance research || news sentiment] -> strategy -> signal -> trader per symbol -> performance -> review -> summary.
- **Trace everything** - Every agent call is one trace entry: agent, brain (LLM or rules) and output.
- **Publish** - A README with the flow diagram and set-up, .env.example but never .env, tests passing, then git push.

## What you'll build

agents/strategy_review.py, agents/lead.py, run.py, a README and a public GitHub repository

**Tools:** ThreadPoolExecutor, Git, GitHub, Claude Code or Codex

## Steps

1. **Prompt for the review agent.**
   Paste into your AI coding assistant:

   ```text
   Create agents/strategy_review.py, NAME='strategy_review', run(performance, strategies) -> (Review, brain): start from DEFAULT_GUIDANCE merged with guidance.json; if trades >= 2 and total return < 0 set verdict 'adjust' and raise entry_threshold by 0.05 (max 0.6); let ask_json() suggest weights; normalise weights; save guidance.json.
   ```

2. **Prompt for the lead agent and the CLI.**
   Paste into your AI coding assistant:

   ```text
   Create agents/lead.py, NAME='lead', run(symbols) that records a plan trace entry, then for each symbol runs finance_research and news_sentiment in parallel with ThreadPoolExecutor, then trading_strategy (with guidance.json), signal_generation and stock_trader; after all symbols runs performance_analysis and strategy_review; ends with a summary from ask_json() and appends the run to runs.jsonl. Add run.py that prints each trace step and the summary.
   ```

3. **Run the whole workflow twice and compare: the second run reads the review's guidance.**

   ```bash
   python run.py NVDA AAPL SPY
   python run.py NVDA AAPL SPY
   cat state/guidance.json
   ```

4. **Run every check.**

   ```bash
   pytest -q
   ```

5. **Ask the assistant for a README, create an empty GitHub repository and push.**
   Paste into your AI coding assistant:

   ```text
   Write README.md with the eight agents, a mermaid flow diagram, set-up (venv, .env from .env.example, OFFLINE=true), how to run run.py, the dashboard and the tests.
   git add -A && git commit -m "Lab 8: review loop, lead agent, README"
   git remote add origin https://github.com/<you>/trading-agents.git && git push -u origin main
   ```

## Verify

pytest -q passes every check; the trace lists lead, finance_research, news_sentiment, trading_strategy, signal_generation, stock_trader, performance_analysis, strategy_review and lead; the second run's strategy uses the threshold in guidance.json; your repository is on GitHub without a .env file.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
