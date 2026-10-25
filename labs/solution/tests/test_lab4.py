"""Lab 4 - Trading Strategy Agent."""
from trading_agents import indicators
from trading_agents.agents import finance_research, news_sentiment, trading_strategy


def test_lab4_votes_cover_every_algorithm():
    fin, _ = finance_research.run("AAPL")
    assert set(indicators.votes(fin["indicators"])) == {"trend", "momentum", "volatility", "vwap", "rsi", "macd"}


def test_lab4_strategy_weights_sum_to_one():
    fin, _ = finance_research.run("SPY")
    sen, _ = news_sentiment.run("SPY")
    strat, _ = trading_strategy.run(fin, sen, None)
    assert abs(sum(strat["weights"].values()) - 1) < 0.01 and -1 <= strat["combined_score"] <= 1
