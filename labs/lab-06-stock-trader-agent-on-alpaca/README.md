# Lab 6 - Build the Stock Trader Agent on Alpaca Paper

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 03:** Execution, Performance and the Feedback Loop  |  **Time:** 30 min

**Learning outcome:** LO3: vibe-code an agent that places long and short market orders on an Alpaca paper account.

Build the broker layer - Alpaca paper trading through alpaca-py, with an offline simulated paper broker of the same interface - and the Stock Trader Agent that sizes the position and buys, sells short, flips or stays out according to the signal.

## Key concepts

- **Paper only** - TradingClient(key, secret, paper=True) - the code never touches a live account.
- **Long, short, flip** - long -> buy; short -> sell short; an opposite position is closed first; already in the same direction -> skip.
- **Position sizing** - Shares = equity x POSITION_PCT / price, rounded down.
- **Same interface offline** - PaperSim keeps cash, positions and fills in state/ so the agent behaves identically without keys.

## What you'll build

trading_agents/broker.py (AlpacaPaper, PaperSim, get_broker) and agents/stock_trader.py

**Tools:** Alpaca paper trading API (alpaca-py), Claude Code or Codex

## Steps

1. **Create a free Alpaca paper account, copy the paper keys into .env.**

   ```bash
   ALPACA_API_KEY=<PAPER-KEY>
   ALPACA_SECRET_KEY=<PAPER-SECRET>
   ```

2. **Prompt for the broker layer.**
   Paste into your AI coding assistant:

   ```text
   Create trading_agents/broker.py with PaperSim (cash 100000, positions with avg price, mark(), position(), positions(), equity(), submit(symbol, side, qty, price) returning status and realized P&L) and AlpacaPaper using alpaca-py TradingClient(paper=True) with the same methods (MarketOrderRequest, TimeInForce.DAY); get_broker() returns AlpacaPaper only when OFFLINE=false and both keys are set.
   ```

3. **Prompt for the agent.**
   Paste into your AI coding assistant:

   ```text
   Create agents/stock_trader.py, NAME='stock_trader', run(signal, price, broker=None) -> (OrderResult, 'code'): null -> no order; same direction already held -> skip; otherwise close the opposite position, then buy (long) or sell short (short) equity*POSITION_PCT//price shares, append each fill to trades.jsonl, and record any broker error instead of raising.
   ```

4. **Run the check offline, then place one live paper order and find it in the Alpaca dashboard.**

   ```bash
   pytest -q tests/test_lab6.py
   OFFLINE=false python -c "from trading_agents.agents import stock_trader as t; print(t.run({'symbol':'SPY','signal':'long'}, 580.0)[0])"
   ```

5. **Commit.**

   ```bash
   git add -A && git commit -m "Lab 6: stock trader agent on Alpaca paper"
   ```

## Verify

tests/test_lab6.py passes: long opens a long position, short closes it and opens a short, null places no order. The live paper order appears under Orders in the Alpaca paper dashboard.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
