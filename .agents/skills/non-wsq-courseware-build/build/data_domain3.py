"""Topic 3 labs - execution, performance and the loop - Build a Multi AI Agents Workflow for Stock Trading (C177)."""

DOMAIN3 = [
    dict(
        num=6, topic=3,
        title="Build the Stock Trader Agent on Alpaca Paper",
        objective="LO3: vibe-code an agent that places long and short market orders on an Alpaca paper account",
        desc=("Build the broker layer - Alpaca paper trading through alpaca-py, with an offline simulated paper broker of "
              "the same interface - and the Stock Trader Agent that sizes the position and buys, sells short, flips or "
              "stays out according to the signal."),
        build="trading_agents/broker.py (AlpacaPaper, PaperSim, get_broker) and agents/stock_trader.py",
        services="Alpaca paper trading API (alpaca-py), Claude Code or Codex",
        concepts=[
            ("Paper only", "TradingClient(key, secret, paper=True) - the code never touches a live account."),
            ("Long, short, flip", "long -> buy; short -> sell short; an opposite position is closed first; already in the same direction -> skip."),
            ("Position sizing", "Shares = equity x POSITION_PCT / price, rounded down."),
            ("Same interface offline", "PaperSim keeps cash, positions and fills in state/ so the agent behaves identically without keys."),
        ],
        steps=[
            ("Create a free Alpaca paper account, copy the paper keys into .env.", "ALPACA_API_KEY=<PAPER-KEY>\nALPACA_SECRET_KEY=<PAPER-SECRET>"),
            ("Prompt for the broker layer.",
             "PROMPT: Create trading_agents/broker.py with PaperSim (cash 100000, positions with avg price, mark(), position(), "
             "positions(), equity(), submit(symbol, side, qty, price) returning status and realized P&L) and AlpacaPaper using "
             "alpaca-py TradingClient(paper=True) with the same methods (MarketOrderRequest, TimeInForce.DAY); get_broker() "
             "returns AlpacaPaper only when OFFLINE=false and both keys are set."),
            ("Prompt for the agent.",
             "PROMPT: Create agents/stock_trader.py, NAME='stock_trader', run(signal, price, broker=None) -> (OrderResult, 'code'): "
             "null -> no order; same direction already held -> skip; otherwise close the opposite position, then buy (long) or "
             "sell short (short) equity*POSITION_PCT//price shares, append each fill to trades.jsonl, and record any broker "
             "error instead of raising."),
            ("Run the check offline, then place one live paper order and find it in the Alpaca dashboard.",
             "pytest -q tests/test_lab6.py\nOFFLINE=false python -c \"from trading_agents.agents import stock_trader as t; print(t.run({'symbol':'SPY','signal':'long'}, 580.0)[0])\""),
            ("Commit.", "git add -A && git commit -m \"Lab 6: stock trader agent on Alpaca paper\""),
        ],
        test=("tests/test_lab6.py passes: long opens a long position, short closes it and opens a short, null places no order. "
              "The live paper order appears under Orders in the Alpaca paper dashboard."),
    ),
    dict(
        num=7, topic=3,
        title="Build the Performance Analysis Agent and the Dashboard",
        objective="LO4: vibe-code an agent that computes return and risk metrics and a dashboard that shows them",
        desc=("Build the agent that records the equity after every run and computes total return, Sharpe ratio, maximum "
              "drawdown, win rate and trade count, then a Streamlit dashboard that runs the workflow and shows the "
              "metrics, the equity curve, the signals and the orders."),
        build="agents/performance_analysis.py (metrics() and run()) and dashboard.py",
        services="Streamlit, pandas, Claude Code or Codex",
        concepts=[
            ("Total return", "Latest equity / starting equity - 1."),
            ("Sharpe ratio", "Mean of per-run returns / their standard deviation x sqrt(252)."),
            ("Maximum drawdown", "The worst fall from a running equity peak."),
            ("Win rate", "Share of closing trades with positive realised P&L."),
        ],
        steps=[
            ("Prompt for the agent.",
             "PROMPT: Create agents/performance_analysis.py, NAME='performance_analysis', metrics(curve, trades) returning "
             "total_return_pct, sharpe, max_drawdown_pct, win_rate_pct and trades, and run(broker=None) that appends the "
             "equity to equity.jsonl, computes the metrics from the equity curve and trades.jsonl, adds open positions, "
             "lets ask_json() write a two-sentence summary, and saves performance.json."),
            ("Prompt for the dashboard.",
             "PROMPT: Create dashboard.py in Streamlit: a symbols box and a 'Run the workflow' button, a five-metric row "
             "(equity, return, Sharpe, max drawdown, win rate) from performance.json, a line chart of equity.jsonl, and the "
             "strategy guidance from guidance.json."),
            ("Run the check and open the dashboard.", "pytest -q tests/test_lab7.py\nstreamlit run dashboard.py"),
            ("Commit.", "git add -A && git commit -m \"Lab 7: performance analysis agent and dashboard\""),
        ],
        test=("tests/test_lab7.py passes: a rising equity curve gives a positive return and zero drawdown; a fall gives a "
              "negative drawdown. The dashboard shows the five metrics after a run."),
    ),
    dict(
        num=8, topic=3,
        title="Close the Loop: Strategy Review, Lead Agent and GitHub",
        objective="LO4: vibe-code the strategy review feedback loop and the lead agent, then publish the project to GitHub",
        desc=("Build the Strategy Review Agent that reads the performance and rewrites the strategy guidance, and the Lead "
              "Agent that orchestrates the whole workflow - the two research agents in parallel, then strategy, signal, "
              "trade, performance and review - and summarises the run. Run it twice to watch the loop change the "
              "strategy, then push your project to your own GitHub repository."),
        build="agents/strategy_review.py, agents/lead.py, run.py, a README and a public GitHub repository",
        services="ThreadPoolExecutor, Git, GitHub, Claude Code or Codex",
        concepts=[
            ("Review rules", "With two or more trades and a negative return, raise the entry threshold by 0.05 and adjust; otherwise keep. The LLM may re-weight the algorithms."),
            ("guidance.json", "The review writes it; the strategy agent reads it on the next run - that is the feedback loop."),
            ("Lead orchestration", "Plan -> [finance research || news sentiment] -> strategy -> signal -> trader per symbol -> performance -> review -> summary."),
            ("Trace everything", "Every agent call is one trace entry: agent, brain (LLM or rules) and output."),
            ("Publish", "A README with the flow diagram and set-up, .env.example but never .env, tests passing, then git push."),
        ],
        steps=[
            ("Prompt for the review agent.",
             "PROMPT: Create agents/strategy_review.py, NAME='strategy_review', run(performance, strategies) -> (Review, brain): "
             "start from DEFAULT_GUIDANCE merged with guidance.json; if trades >= 2 and total return < 0 set verdict 'adjust' "
             "and raise entry_threshold by 0.05 (max 0.6); let ask_json() suggest weights; normalise weights; save guidance.json."),
            ("Prompt for the lead agent and the CLI.",
             "PROMPT: Create agents/lead.py, NAME='lead', run(symbols) that records a plan trace entry, then for each symbol runs "
             "finance_research and news_sentiment in parallel with ThreadPoolExecutor, then trading_strategy (with guidance.json), "
             "signal_generation and stock_trader; after all symbols runs performance_analysis and strategy_review; ends with a "
             "summary from ask_json() and appends the run to runs.jsonl. Add run.py that prints each trace step and the summary."),
            ("Run the whole workflow twice and compare: the second run reads the review's guidance.",
             "python run.py NVDA AAPL SPY\npython run.py NVDA AAPL SPY\ncat state/guidance.json"),
            ("Run every check.", "pytest -q"),
            ("Ask the assistant for a README, create an empty GitHub repository and push.",
             "PROMPT: Write README.md with the eight agents, a mermaid flow diagram, set-up (venv, .env from .env.example, "
             "OFFLINE=true), how to run run.py, the dashboard and the tests.\n"
             "git add -A && git commit -m \"Lab 8: review loop, lead agent, README\"\n"
             "git remote add origin https://github.com/<you>/trading-agents.git && git push -u origin main"),
        ],
        test=("pytest -q passes every check; the trace lists lead, finance_research, news_sentiment, trading_strategy, "
              "signal_generation, stock_trader, performance_analysis, strategy_review and lead; the second run's strategy uses "
              "the threshold in guidance.json; your repository is on GitHub without a .env file."),
    ),
]
