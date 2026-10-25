"""Lab 3 - News Sentiment Agent (Reddit + NewsAPI)."""
from trading_agents.agents import news_sentiment


def test_lab3_news_sentiment_reads_reddit_and_news():
    out, _ = news_sentiment.run("NVDA")
    assert -1 <= out["score"] <= 1
    assert out["reddit"]["posts"] > 0 and out["news"]["articles"] > 0
