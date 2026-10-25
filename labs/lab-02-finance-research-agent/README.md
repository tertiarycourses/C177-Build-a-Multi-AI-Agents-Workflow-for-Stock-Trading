# Lab 2 - Build the Finance Research Agent

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 02:** Building the Research and Decision Agents  |  **Time:** 35 min

**Learning outcome:** LO2: vibe-code an agent that gathers Twelve Data candles, Yahoo Finance and Equibles company data.

Direct your assistant to build three data clients - Twelve Data (1-minute, 15-minute and 1-hour candles), Yahoo Finance (company profile and ratios through yfinance) and Equibles (valuation multiples, short interest and insider transactions) - plus the indicator module, then the Finance Research Agent that combines them into one FinanceReport.

## Key concepts

- **Three intervals** - 1min for entry timing, 15min for the intraday trend the indicators use, 1h for session context.
- **Twelve Data** - GET https://api.twelvedata.com/time_series with symbol, interval and an 'apikey' Authorization header.
- **Equibles** - Bearer-key REST API: /stocks/{symbol}/valuation-multiples, /short-interest and /insider-transactions.
- **Indicators in code** - EMA 20/50, 10-bar momentum, RSI 14, MACD 12/26/9, VWAP and Bollinger bands - computed with pandas, never by the LLM.

## What you'll build

trading_agents/data/twelvedata.py, yahoo.py, equibles.py, trading_agents/indicators.py and agents/finance_research.py

**Tools:** Twelve Data API, yfinance, Equibles API, pandas, Claude Code or Codex

## Steps

1. **Prompt for the Twelve Data client.**
   Paste into your AI coding assistant:

   ```text
   Create trading_agents/data/twelvedata.py with INTERVALS=('1min','15min','1h') and candles(symbol, interval) that calls https://api.twelvedata.com/time_series (outputsize 300, order asc, header Authorization: apikey <TWELVEDATA_API_KEY>) and returns an OHLCV DataFrame indexed by timestamp. When OFFLINE=true or the key is empty, return sample.candles().
   ```

2. **Prompt for the Yahoo Finance and Equibles clients.**
   Paste into your AI coding assistant:

   ```text
   Create data/yahoo.py company(symbol) returning shortName, sector, marketCap, trailingPE, forwardPE, profitMargins, revenueGrowth, debtToEquity, beta and 52-week range from yfinance, and data/equibles.py company(symbol) calling https://api.equibles.com/v1/stocks/{symbol}/valuation-multiples, /short-interest?limit=3 and /insider-transactions?limit=10 with a Bearer key, recording a section's error instead of failing. Both use sample.load() offline.
   ```

3. **Prompt for the indicators module.**
   Paste into your AI coding assistant:

   ```text
   Create trading_agents/indicators.py with ema, rsi, macd, vwap, bollinger, snapshot(df) returning the latest close, ema_fast(20), ema_slow(50), momentum_pct(10), rsi, macd, macd_signal, vwap, bb_low, bb_high, and votes(snapshot) returning +1/0/-1 for trend, momentum, volatility, vwap, rsi, macd.
   ```

4. **Prompt for the agent itself.**
   Paste into your AI coding assistant:

   ```text
   Create agents/finance_research.py with NAME='finance_research' and run(symbol) -> (FinanceReport, brain): fetch all three intervals, compute indicators.snapshot on the 15min candles, add Yahoo and Equibles data, build a one-line summary as the fallback and let ask_json() rewrite only the summary.
   ```

5. **Review the code, run the check offline, then live with your keys, and commit.**

   ```bash
   pytest -q tests/test_lab2.py
   OFFLINE=false python -c "from trading_agents.agents import finance_research as f; print(f.run('NVDA')[0]['summary'])"
   git add -A && git commit -m "Lab 2: finance research agent"
   ```

## Verify

tests/test_lab2.py passes: the report has candles for 1min, 15min and 1h, a positive last_price, an RSI value, company and Equibles data. With keys set, the live summary names the real last price.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
