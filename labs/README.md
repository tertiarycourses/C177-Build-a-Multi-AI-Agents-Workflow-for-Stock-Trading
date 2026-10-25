# Labs - Build a Multi AI Agents Workflow for Stock Trading (C177)

Eight labs build one project from scratch with AI vibe coding. Each lab: read the concepts, paste the prompts into Claude Code or Codex, review the code, run the lab's check, commit.

| Lab | Title | Time | Check |
|---|---|---|---|
| 1 | [Scaffold the Project and the Agent Message Contract](lab-01-scaffold-the-project-and-the-agent-contract/README.md) | 35 min | `tests/test_lab1.py` |
| 2 | [Build the Finance Research Agent](lab-02-finance-research-agent/README.md) | 35 min | `tests/test_lab2.py` |
| 3 | [Build the News Sentiment Agent with Reddit and NewsAPI](lab-03-news-sentiment-agent-with-reddit/README.md) | 35 min | `tests/test_lab3.py` |
| 4 | [Build the Trading Strategy Agent](lab-04-trading-strategy-agent/README.md) | 35 min | `tests/test_lab4.py` |
| 5 | [Build the Signal Generation Agent](lab-05-signal-generation-agent/README.md) | 20 min | `tests/test_lab5.py` |
| 6 | [Build the Stock Trader Agent on Alpaca Paper](lab-06-stock-trader-agent-on-alpaca/README.md) | 30 min | `tests/test_lab6.py` |
| 7 | [Build the Performance Analysis Agent and the Dashboard](lab-07-performance-analysis-agent-and-dashboard/README.md) | 30 min | `tests/test_lab7.py` |
| 8 | [Close the Loop: Strategy Review, Lead Agent and GitHub](lab-08-strategy-review-lead-agent-and-github/README.md) | 65 min | `tests/test_lab8.py` |

## Reference solution

[`solution/`](solution/) holds the complete working project (all eight agents, the dashboard and the acceptance checks). It runs offline: `cd labs/solution && pip install -e .[dev] && OFFLINE=true python run.py`.

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
