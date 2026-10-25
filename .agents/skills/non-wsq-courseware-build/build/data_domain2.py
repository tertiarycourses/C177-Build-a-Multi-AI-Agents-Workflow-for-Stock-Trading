"""Topic 2 labs - research and decision agents - Build a Multi AI Agents Workflow for Stock Trading (C177)."""

DOMAIN2 = [
    dict(
        num=2, topic=2,
        title="Build the Finance Research Agent",
        objective="LO2: vibe-code an agent that gathers Twelve Data candles, Yahoo Finance and Equibles company data",
        desc=("Direct your assistant to build three data clients - Twelve Data (1-minute, 15-minute and 1-hour candles), "
              "Yahoo Finance (company profile and ratios through yfinance) and Equibles (valuation multiples, short "
              "interest and insider transactions) - plus the indicator module, then the Finance Research Agent that "
              "combines them into one FinanceReport."),
        build="trading_agents/data/twelvedata.py, yahoo.py, equibles.py, trading_agents/indicators.py and agents/finance_research.py",
        services="Twelve Data API, yfinance, Equibles API, pandas, Claude Code or Codex",
        concepts=[
            ("Three intervals", "1min for entry timing, 15min for the intraday trend the indicators use, 1h for session context."),
            ("Twelve Data", "GET https://api.twelvedata.com/time_series with symbol, interval and an 'apikey' Authorization header."),
            ("Equibles", "Bearer-key REST API: /stocks/{symbol}/valuation-multiples, /short-interest and /insider-transactions."),
            ("Indicators in code", "EMA 20/50, 10-bar momentum, RSI 14, MACD 12/26/9, VWAP and Bollinger bands - computed with pandas, never by the LLM."),
        ],
        steps=[
            ("Prompt for the Twelve Data client.",
             "PROMPT: Create trading_agents/data/twelvedata.py with INTERVALS=('1min','15min','1h') and "
             "candles(symbol, interval) that calls https://api.twelvedata.com/time_series (outputsize 300, order asc, "
             "header Authorization: apikey <TWELVEDATA_API_KEY>) and returns an OHLCV DataFrame indexed by timestamp. "
             "When OFFLINE=true or the key is empty, return sample.candles()."),
            ("Prompt for the Yahoo Finance and Equibles clients.",
             "PROMPT: Create data/yahoo.py company(symbol) returning shortName, sector, marketCap, trailingPE, "
             "forwardPE, profitMargins, revenueGrowth, debtToEquity, beta and 52-week range from yfinance, and "
             "data/equibles.py company(symbol) calling https://api.equibles.com/v1/stocks/{symbol}/valuation-multiples, "
             "/short-interest?limit=3 and /insider-transactions?limit=10 with a Bearer key, recording a section's "
             "error instead of failing. Both use sample.load() offline."),
            ("Prompt for the indicators module.",
             "PROMPT: Create trading_agents/indicators.py with ema, rsi, macd, vwap, bollinger, snapshot(df) returning "
             "the latest close, ema_fast(20), ema_slow(50), momentum_pct(10), rsi, macd, macd_signal, vwap, bb_low, "
             "bb_high, and votes(snapshot) returning +1/0/-1 for trend, momentum, volatility, vwap, rsi, macd."),
            ("Prompt for the agent itself.",
             "PROMPT: Create agents/finance_research.py with NAME='finance_research' and run(symbol) -> (FinanceReport, "
             "brain): fetch all three intervals, compute indicators.snapshot on the 15min candles, add Yahoo and "
             "Equibles data, build a one-line summary as the fallback and let ask_json() rewrite only the summary."),
            ("Review the code, run the check offline, then live with your keys, and commit.",
             "pytest -q tests/test_lab2.py\nOFFLINE=false python -c \"from trading_agents.agents import finance_research as f; print(f.run('NVDA')[0]['summary'])\"\n"
             "git add -A && git commit -m \"Lab 2: finance research agent\""),
        ],
        test=("tests/test_lab2.py passes: the report has candles for 1min, 15min and 1h, a positive last_price, an RSI value, "
              "company and Equibles data. With keys set, the live summary names the real last price."),
    ),
    dict(
        num=3, topic=2,
        title="Build the News Sentiment Agent with Reddit and NewsAPI",
        objective="LO2: vibe-code the Reddit API integration and an agent that scores Reddit and news sentiment",
        desc=("Integrate the Reddit API with the OAuth application-only flow, add a NewsAPI.org client and a small finance "
              "lexicon scorer, then build the News Sentiment Agent that blends both sources into one score from -1 to +1 "
              "and lets the LLM refine it."),
        build="trading_agents/data/reddit.py, data/newsapi.py, trading_agents/sentiment.py and agents/news_sentiment.py",
        services="Reddit API (script app), NewsAPI.org, httpx, Claude Code or Codex",
        concepts=[
            ("Reddit OAuth", "POST https://www.reddit.com/api/v1/access_token with grant_type=client_credentials and your app's id/secret; then call https://oauth.reddit.com with 'bearer <token>' and a descriptive User-Agent."),
            ("Where traders talk", "Search r/stocks, r/wallstreetbets and r/investing for the symbol, newest first, past week."),
            ("NewsAPI", "GET https://newsapi.org/v2/everything?q=<symbol> with the X-Api-Key header."),
            ("Blend, then refine", "Lexicon scores give a deterministic base (news 60%, Reddit 40%); the LLM may refine the score but never leaves -1..1."),
        ],
        steps=[
            ("Create a Reddit 'script' app at reddit.com/prefs/apps and put the id, secret and a User-Agent in .env.",
             "REDDIT_CLIENT_ID=<YOUR-ID>\nREDDIT_CLIENT_SECRET=<YOUR-SECRET>\nREDDIT_USER_AGENT=trading-agents/1.0 by <your-username>"),
            ("Prompt for the Reddit integration.",
             "PROMPT: Create trading_agents/data/reddit.py: token() gets an application-only OAuth token (client_credentials) "
             "from https://www.reddit.com/api/v1/access_token; posts(symbol) searches each subreddit in REDDIT_SUBREDDITS via "
             "https://oauth.reddit.com/r/<sub>/search (q=symbol, restrict_sr=1, sort=new, t=week) and returns subreddit, "
             "title, text, score, comments, url. Always send REDDIT_USER_AGENT. Offline or without keys use sample.load('reddit')."),
            ("Prompt for the NewsAPI client and the lexicon scorer.",
             "PROMPT: Create data/newsapi.py headlines(symbol) using https://newsapi.org/v2/everything (X-Api-Key header) and "
             "trading_agents/sentiment.py with score(text) from small positive/negative finance word lists and average(texts)."),
            ("Prompt for the agent.",
             "PROMPT: Create agents/news_sentiment.py, NAME='news_sentiment', run(symbol) -> (SentimentReport, brain): score "
             "Reddit and news separately, combine 0.4*reddit + 0.6*news as the fallback score, ask_json() may refine score and "
             "summary, then clamp score to -1..1."),
            ("Run the check offline and live, and commit.",
             "pytest -q tests/test_lab3.py\nOFFLINE=false python -c \"from trading_agents.data import reddit; print(len(reddit.posts('NVDA')))\"\n"
             "git add -A && git commit -m \"Lab 3: news sentiment agent with Reddit\""),
        ],
        test=("tests/test_lab3.py passes: score is between -1 and 1 and both Reddit posts and news articles were read. With "
              "keys set, reddit.posts('NVDA') returns recent posts from the configured subreddits."),
    ),
    dict(
        num=4, topic=2,
        title="Build the Trading Strategy Agent",
        objective="LO3: vibe-code an agent that merges finance and sentiment into a weighted mix of trading algorithms",
        desc=("Build the agent that turns the two research reports into a strategy: the six algorithm votes come from code, "
              "the agent chooses one algorithm or a weighted mix, adds the sentiment, and reads the strategy review's "
              "guidance so the next lab's feedback loop has something to change."),
        build="agents/trading_strategy.py with DEFAULT_GUIDANCE and a combined score from -1 to +1",
        services="indicators.py votes, ask_json(), Claude Code or Codex",
        concepts=[
            ("Six algorithms", "Trend (EMA 20 vs 50), momentum (10-bar change), volatility (Bollinger breakout), VWAP (price vs VWAP), RSI (30/70 reversal) and MACD (line vs signal)."),
            ("Single or mix", "The agent may pick one algorithm or weight several; weights are normalised to sum to 1."),
            ("Combined score", "(1 - sentiment weight) x weighted votes + sentiment weight x sentiment score."),
            ("Guidance in, strategy out", "DEFAULT_GUIDANCE (trend 0.4, MACD 0.35, RSI 0.25, threshold 0.3, sentiment weight 0.3) until the review agent writes guidance.json."),
        ],
        steps=[
            ("Prompt for the agent.",
             "PROMPT: Create agents/trading_strategy.py, NAME='trading_strategy', DEFAULT_GUIDANCE as described, and "
             "run(finance, sentiment, guidance) -> (Strategy, brain). Compute votes with indicators.votes() - never ask the "
             "LLM for indicator values. Let ask_json() choose algorithms and weights, keep only names in ALGORITHMS, "
             "normalise weights to 1, and compute combined_score and entry_threshold from the guidance."),
            ("Review: confirm the LLM can only choose weights, never invent votes or prices.",
             "grep -n \"votes\" trading_agents/agents/trading_strategy.py"),
            ("Try three mixes by hand and compare the combined score.",
             "python -c \"from trading_agents.agents import finance_research as f, news_sentiment as n, trading_strategy as t;"
             " fi=f.run('AAPL')[0]; se=n.run('AAPL')[0];"
             " [print(w, t.run(fi, se, {'weights': w})[0]['combined_score']) for w in ({'trend':1}, {'rsi':1}, {'macd':0.5,'vwap':0.5})]\""),
            ("Run the check and commit.",
             "pytest -q tests/test_lab4.py\ngit add -A && git commit -m \"Lab 4: trading strategy agent\""),
        ],
        test=("tests/test_lab4.py passes: votes cover all six algorithms and the strategy's weights sum to 1. Changing the "
              "weights changes combined_score."),
    ),
    dict(
        num=5, topic=2,
        title="Build the Signal Generation Agent",
        objective="LO3: vibe-code an agent that turns the strategy into a long, short or null signal",
        desc=("Build the small but critical agent that converts the combined score into exactly one signal with a "
              "confidence, using the entry threshold from the guidance, and guard against any invalid LLM answer."),
        build="agents/signal_generation.py with rule_signal() and run()",
        services="ask_json(), Claude Code or Codex",
        concepts=[
            ("Threshold rule", "long if score >= threshold, short if score <= -threshold, otherwise null."),
            ("Confidence", "The size of the combined score, clamped to 0..1."),
            ("Guard the output", "Any answer other than long, short or null is replaced by the rule signal."),
        ],
        steps=[
            ("Prompt for the agent.",
             "PROMPT: Create agents/signal_generation.py, NAME='signal_generation', rule_signal(score, threshold) and "
             "run(strategy) -> (TradeSignal, brain) as specified; validate the LLM's signal and clamp confidence to 0..1."),
            ("Run the check and print the signals for three symbols.",
             "pytest -q tests/test_lab5.py\npython -c \"from trading_agents.agents import signal_generation as s; print(s.rule_signal(0.5,0.3), s.rule_signal(-0.5,0.3), s.rule_signal(0.1,0.3))\""),
            ("Commit.", "git add -A && git commit -m \"Lab 5: signal generation agent\""),
        ],
        test="tests/test_lab5.py passes and the three sample scores print long, short and null.",
    ),
]
