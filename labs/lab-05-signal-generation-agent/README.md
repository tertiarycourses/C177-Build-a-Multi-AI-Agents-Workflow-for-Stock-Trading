# Lab 5 - Build the Signal Generation Agent

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 02:** Building the Research and Decision Agents  |  **Time:** 20 min

**Learning outcome:** LO3: vibe-code an agent that turns the strategy into a long, short or null signal.

Build the small but critical agent that converts the combined score into exactly one signal with a confidence, using the entry threshold from the guidance, and guard against any invalid LLM answer.

## Key concepts

- **Threshold rule** - long if score >= threshold, short if score <= -threshold, otherwise null.
- **Confidence** - The size of the combined score, clamped to 0..1.
- **Guard the output** - Any answer other than long, short or null is replaced by the rule signal.

## What you'll build

agents/signal_generation.py with rule_signal() and run()

**Tools:** ask_json(), Claude Code or Codex

## Steps

1. **Prompt for the agent.**
   Paste into your AI coding assistant:

   ```text
   Create agents/signal_generation.py, NAME='signal_generation', rule_signal(score, threshold) and run(strategy) -> (TradeSignal, brain) as specified; validate the LLM's signal and clamp confidence to 0..1.
   ```

2. **Run the check and print the signals for three symbols.**

   ```bash
   pytest -q tests/test_lab5.py
   python -c "from trading_agents.agents import signal_generation as s; print(s.rule_signal(0.5,0.3), s.rule_signal(-0.5,0.3), s.rule_signal(0.1,0.3))"
   ```

3. **Commit.**

   ```bash
   git add -A && git commit -m "Lab 5: signal generation agent"
   ```

## Verify

tests/test_lab5.py passes and the three sample scores print long, short and null.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
