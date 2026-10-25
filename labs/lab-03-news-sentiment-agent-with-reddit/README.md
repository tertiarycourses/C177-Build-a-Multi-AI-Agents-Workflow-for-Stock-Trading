# Lab 3 - Build the News Sentiment Agent with Reddit and NewsAPI

**Course:** Build a Multi AI Agents Workflow for Stock Trading (C177)  |  **Topic 02:** Building the Research and Decision Agents  |  **Time:** 35 min

**Learning outcome:** LO2: vibe-code the Reddit API integration and an agent that scores Reddit and news sentiment.

Integrate the Reddit API with the OAuth application-only flow, add a NewsAPI.org client and a small finance lexicon scorer, then build the News Sentiment Agent that blends both sources into one score from -1 to +1 and lets the LLM refine it.

## Key concepts

- **Reddit OAuth** - POST https://www.reddit.com/api/v1/access_token with grant_type=client_credentials and your app's id/secret; then call https://oauth.reddit.com with 'bearer <token>' and a descriptive User-Agent.
- **Where traders talk** - Search r/stocks, r/wallstreetbets and r/investing for the symbol, newest first, past week.
- **NewsAPI** - GET https://newsapi.org/v2/everything?q=<symbol> with the X-Api-Key header.
- **Blend, then refine** - Lexicon scores give a deterministic base (news 60%, Reddit 40%); the LLM may refine the score but never leaves -1..1.

## What you'll build

trading_agents/data/reddit.py, data/newsapi.py, trading_agents/sentiment.py and agents/news_sentiment.py

**Tools:** Reddit API (script app), NewsAPI.org, httpx, Claude Code or Codex

## Steps

1. **Create a Reddit 'script' app at reddit.com/prefs/apps and put the id, secret and a User-Agent in .env.**

   ```bash
   REDDIT_CLIENT_ID=<YOUR-ID>
   REDDIT_CLIENT_SECRET=<YOUR-SECRET>
   REDDIT_USER_AGENT=trading-agents/1.0 by <your-username>
   ```

2. **Prompt for the Reddit integration.**
   Paste into your AI coding assistant:

   ```text
   Create trading_agents/data/reddit.py: token() gets an application-only OAuth token (client_credentials) from https://www.reddit.com/api/v1/access_token; posts(symbol) searches each subreddit in REDDIT_SUBREDDITS via https://oauth.reddit.com/r/<sub>/search (q=symbol, restrict_sr=1, sort=new, t=week) and returns subreddit, title, text, score, comments, url. Always send REDDIT_USER_AGENT. Offline or without keys use sample.load('reddit').
   ```

3. **Prompt for the NewsAPI client and the lexicon scorer.**
   Paste into your AI coding assistant:

   ```text
   Create data/newsapi.py headlines(symbol) using https://newsapi.org/v2/everything (X-Api-Key header) and trading_agents/sentiment.py with score(text) from small positive/negative finance word lists and average(texts).
   ```

4. **Prompt for the agent.**
   Paste into your AI coding assistant:

   ```text
   Create agents/news_sentiment.py, NAME='news_sentiment', run(symbol) -> (SentimentReport, brain): score Reddit and news separately, combine 0.4*reddit + 0.6*news as the fallback score, ask_json() may refine score and summary, then clamp score to -1..1.
   ```

5. **Run the check offline and live, and commit.**

   ```bash
   pytest -q tests/test_lab3.py
   OFFLINE=false python -c "from trading_agents.data import reddit; print(len(reddit.posts('NVDA')))"
   git add -A && git commit -m "Lab 3: news sentiment agent with Reddit"
   ```

## Verify

tests/test_lab3.py passes: score is between -1 and 1 and both Reddit posts and news articles were read. With keys set, reddit.posts('NVDA') returns recent posts from the configured subreddits.

## Reference solution

If you are stuck, compare with the trainer's reference project in [`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).

> Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is synthetic and for training only; nothing in this course is investment advice.
