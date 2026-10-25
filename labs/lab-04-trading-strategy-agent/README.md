# Lab 4 - Build the Trading Strategy Agent

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 02:** Building the Research and Decision Agents  |  **Time:** 35 min

**Learning outcome:** LO3: vibe-code an agent that merges finance and sentiment into a weighted mix of trading algorithms.

Build the agent that turns the two research reports into a strategy: the six algorithm votes come from code, the agent chooses one algorithm or a weighted mix, adds the sentiment, and reads the strategy review's guidance so the next lab's feedback loop has something to change.

## Key concepts

- **Six algorithms** - Trend (EMA 20 vs 50), momentum (10-bar change), volatility (Bollinger breakout), VWAP (price vs VWAP), RSI (30/70 reversal) and MACD (line vs signal).
- **Single or mix** - The agent may pick one algorithm or weight several; weights are normalised to sum to 1.
- **Combined score** - (1 - sentiment weight) x weighted votes + sentiment weight x sentiment score.
- **Guidance in, strategy out** - DEFAULT_GUIDANCE (trend 0.4, MACD 0.35, RSI 0.25, threshold 0.3, sentiment weight 0.3) until the review agent writes guidance.json.

## What you'll build

agents/trading_strategy.py with DEFAULT_GUIDANCE and a combined score from -1 to +1

**Tools:** indicators.py votes, ask_json(), Claude Code or Codex

## Steps

1. **Prompt for the agent.**
   Paste into your AI coding assistant:

   ```text
   Create agents/trading_strategy.py, NAME='trading_strategy', DEFAULT_GUIDANCE as described, and run(finance, sentiment, guidance) -> (Strategy, brain). Compute votes with indicators.votes() - never ask the LLM for indicator values. Let ask_json() choose algorithms and weights, keep only names in ALGORITHMS, normalise weights to 1, and compute combined_score and entry_threshold from the guidance.
   ```

2. **Review: confirm the LLM can only choose weights, never invent votes or prices.**

   ```bash
   grep -n "votes" trading_agents/agents/trading_strategy.py
   ```

3. **Try three mixes by hand and compare the combined score.**

   ```bash
   python -c "from trading_agents.agents import finance_research as f, news_sentiment as n, trading_strategy as t; fi=f.run('AAPL')[0]; se=n.run('AAPL')[0]; [print(w, t.run(fi, se, {'weights': w})[0]['combined_score']) for w in ({'trend':1}, {'rsi':1}, {'macd':0.5,'vwap':0.5})]"
   ```

4. **Run the check and commit.**

   ```bash
   pytest -q tests/test_lab4.py
   git add -A && git commit -m "Lab 4: trading strategy agent"
   ```

## Verify

tests/test_lab4.py passes: votes cover all six algorithms and the strategy's weights sum to 1. Changing the weights changes combined_score.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
