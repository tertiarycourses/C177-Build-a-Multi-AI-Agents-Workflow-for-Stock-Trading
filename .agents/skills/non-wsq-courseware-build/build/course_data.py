"""SINGLE SOURCE OF TRUTH — Build a Multi AI Agents Workflow for Stock Trading (C177).

Non-WSQ commercial short course: no assessment, no funding content, no TRAQOM, no attendance rule.
Every artifact (PPT, LP, LG, lab READMEs) is generated from this file + data_domain1..3.py.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Build a Multi AI Agents Workflow for Stock Trading (C177)"
SHORT_TITLE  = "Build a Multi AI Agents Workflow for Stock Trading (C177)"
COURSE_CODE  = "C177"
VERSION      = "v2.0"
VERSION_DATE = "25 October 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr Alfred Ang"
TRAINER_CERT = "PhD; ACTA; DACE; Executive Programme in Algorithmic Trading (QuantInsti)"
TRAINER_DELIVERS = "agentic AI, multi-agent systems, AI vibe coding, algorithmic trading and quantitative finance"
DAYS         = 1
DAY_MINUTES  = 450                     # 9:30am - 5:30pm, 7.5 instructional hours, 30-minute lunch
MODE         = "Instructor-led, hands-on AI vibe coding labs"
DAILY_TIMING = "9:30 am – 5:30 pm (7.5 instructional hours; 30-minute lunch)"
DAILY_TIMING_SHORT = "9:30am–5:30pm · 7.5 hours · 30-minute lunch"
MORNING_LABEL = "Morning · 9:30am–12:35pm"
AFTERNOON_LABEL = "Afternoon · 1:05pm–5:30pm"
ONE_DAY_HEADING = "Lesson Plan — One Day, 7.5 hours"
PREREQUISITE = ("AI Powered Quantitative Trading Fundamentals (C728) - the course that demonstrates this multi AI "
                "agents trading system; C177 teaches you to build it from scratch")
DARK_THEME   = False

COMPANY = "Lion City Capital (fictitious paper-trading desk)"

LAB_SLUGS = {
    1: "scaffold-the-project-and-the-agent-contract",
    2: "finance-research-agent",
    3: "news-sentiment-agent-with-reddit",
    4: "trading-strategy-agent",
    5: "signal-generation-agent",
    6: "stock-trader-agent-on-alpaca",
    7: "performance-analysis-agent-and-dashboard",
    8: "strategy-review-lead-agent-and-github",
}

ICE_BREAKER = [
    "Prerequisite check: what did you run in AI Powered Quantitative Trading Fundamentals (C728)?",
    "Your name, your role and what you trade or analyse (stocks, ETFs, none yet).",
    "Which AI coding assistant have you used - Claude Code, Codex, Cursor, Copilot or none?",
    "One trading decision you would like an AI agent to help you make.",
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Design a multi AI agents trading workflow: the eight agent roles, the message contract between them and a lead agent that orchestrates the flow.",
    "LO2: Vibe-code the research agents that gather Twelve Data candles, Yahoo Finance and Equibles company data, and Reddit and NewsAPI sentiment.",
    "LO3: Vibe-code the decision and execution agents that formulate a strategy from trend, momentum, volatility, VWAP, RSI and MACD, generate long, short or null signals and place orders on an Alpaca paper account.",
    "LO4: Close the loop with a performance dashboard and a strategy review agent, orchestrate the full workflow and publish the project to GitHub.",
]
LO_TITLES = ["Design the Workflow", "Build the Research Agents", "Build Decision and Execution", "Close the Loop and Publish"]

# ------------------------------------------------------------------ topics
TOPICS = [
    dict(num=1, code="01",
         title="Designing a Multi AI Agents Trading Workflow",
         subtitle="Agent roles · message contract · lead orchestration · the AI vibe coding loop",
         concepts=[
            ("Agentic workflow", "Several specialised agents, each with one job, its own instructions and its own data tools, coordinated by a lead agent."),
            ("The eight agents", "Lead, Finance Research, News Sentiment, Trading Strategy, Signal Generation, Stock Trader, Performance Analysis and Strategy Review."),
            ("Message contract", "Every agent returns one typed JSON object; the next agent reads only that object. The contract is what makes AI-written code fit together."),
            ("AI vibe coding loop", "Spec -> prompt -> generate -> review -> test -> commit. You own the design and the checks; the coding agent writes the code."),
            ("Code computes, the LLM judges", "Indicators, maths and order sizes are computed in code; the LLM chooses, weighs and explains. Every agent has a rule-based fallback."),
            ("Paper trading only", "All orders go to an Alpaca PAPER account or the offline simulator. Nothing in this course is investment advice."),
         ]),
    dict(num=2, code="02",
         title="Building the Research and Decision Agents",
         subtitle="Twelve Data · Yahoo Finance · Equibles · Reddit · NewsAPI · strategy algorithms · signals",
         concepts=[
            ("Multi-timeframe data", "1-minute, 15-minute and 1-hour candles answer different questions: entry timing, intraday trend and session context."),
            ("Fundamentals and alternative data", "Yahoo Finance company ratios and Equibles valuation, short-interest and insider data put the price action in context."),
            ("Sentiment as a signal", "Reddit chatter and news headlines are scored from -1 to +1; news is weighted above social posts."),
            ("Algorithm mix", "Trend, momentum, volatility breakout, VWAP, RSI and MACD each vote +1, 0 or -1; the strategy agent weights the votes and the sentiment."),
            ("Long, short or null", "A signal fires only when the combined score clears the entry threshold; otherwise the agent stays out."),
         ]),
    dict(num=3, code="03",
         title="Execution, Performance and the Feedback Loop",
         subtitle="Alpaca paper orders · performance metrics · strategy review · lead orchestration · GitHub",
         concepts=[
            ("Automated paper execution", "The stock trader agent turns a signal into a market order on Alpaca paper: long buys, short sells short, null does nothing."),
            ("Performance metrics", "Total return, Sharpe ratio, maximum drawdown and win rate measure whether the agents add value."),
            ("Feedback loop", "The strategy review agent reads the performance and rewrites the guidance the strategy agent uses next run."),
            ("Orchestration", "The lead agent plans the run, runs the two research agents in parallel and the rest in sequence, and writes the summary."),
            ("Publish safely", "Push to GitHub with .env ignored, keys in environment variables only, a README and passing tests."),
         ]),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {1: "From Design to a Self-Improving Multi AI Agents Trading Desk"}


# ------------------------------------------------------------------ schedule (450 min + 30-min lunch)
def SCHEDULE(lab_titles):
    return {
        1: (DAY_THEMES[1], [
            ("9:30", "9:45", 15, "admin", "Welcome, course outcomes, safety boundary (paper trading only) and set-up check"),
            ("9:45", "10:15", 30, "topic", "Topic 1 - the eight agents, the message contract, lead orchestration and the AI vibe coding loop"),
            ("10:15", "10:50", 35, "lab", "Hands-on: " + lab_titles([1])),
            ("10:50", "11:10", 20, "topic", "Topic 2 - multi-timeframe candles, company fundamentals and Equibles data"),
            ("11:10", "11:45", 35, "lab", "Hands-on: " + lab_titles([2])),
            ("11:45", "12:00", 15, "topic", "Topic 2 - sentiment from Reddit and news, Reddit OAuth"),
            ("12:00", "12:35", 35, "lab", "Hands-on: " + lab_titles([3])),
            ("12:35", "13:05", 30, "lunch", "Lunch break"),
            ("13:05", "13:20", 15, "topic", "Topic 2 - trend, momentum, volatility, VWAP, RSI and MACD as votes; mixing algorithms"),
            ("13:20", "13:55", 35, "lab", "Hands-on: " + lab_titles([4])),
            ("13:55", "14:05", 10, "topic", "Topic 2 - from a strategy score to a long, short or null signal"),
            ("14:05", "14:25", 20, "lab", "Hands-on: " + lab_titles([5])),
            ("14:25", "14:40", 15, "topic", "Topic 3 - automated execution on Alpaca paper: long, short and flipping"),
            ("14:40", "15:10", 30, "lab", "Hands-on: " + lab_titles([6])),
            ("15:10", "15:25", 15, "topic", "Topic 3 - return, Sharpe, drawdown and win rate; building a dashboard"),
            ("15:25", "15:55", 30, "lab", "Hands-on: " + lab_titles([7])),
            ("15:55", "16:10", 15, "topic", "Topic 3 - feedback loops, lead orchestration and publishing to GitHub"),
            ("16:10", "17:15", 65, "lab", "Hands-on: " + lab_titles([8])),
            ("17:15", "17:30", 15, "recap", "Run the full workflow, recap, next steps and Q&A"),
        ]),
    }


# ------------------------------------------------------------------ deck overview section
COURSE_OVERVIEW = dict(
    section_title="Course Fundamentals",
    concepts_title="What You Will Build Today",
    concepts=[
        ("Lead Agent", "Orchestrates the whole flow and writes the run summary."),
        ("Finance Research Agent", "Twelve Data 1min / 15min / 1h candles, Yahoo Finance and Equibles company data."),
        ("News Sentiment Agent", "Reddit posts and NewsAPI headlines scored into one sentiment."),
        ("Trading Strategy Agent", "Merges finance and sentiment; picks or mixes trend, momentum, volatility, VWAP, RSI and MACD."),
        ("Signal Generation Agent", "Turns the strategy into a long, short or null signal."),
        ("Stock Trader Agent", "Places the order on the Alpaca paper account."),
        ("Performance Analysis Agent", "Computes return and risk metrics for the dashboard."),
        ("Strategy Review Agent", "Reviews the results and updates the strategy agent's guidance."),
    ],
    framework_title="The Workflow",
    framework=[
        ("1. Lead", "Plans the run for each symbol."),
        ("2. Research", "Finance Research and News Sentiment run in parallel."),
        ("3. Strategy", "Votes from six algorithms, weighted with sentiment."),
        ("4. Signal", "Long, short or null."),
        ("5. Trade", "Market order on Alpaca paper."),
        ("6. Performance", "Return, Sharpe, drawdown, win rate."),
        ("7. Review", "New guidance for the next run - the feedback loop."),
    ],
    statement=dict(headline="You design the agents. The AI writes the code. The tests decide.",
                   body="Every lab gives you a spec and a prompt for your AI coding assistant, then a check that proves the generated agent honours the contract.",
                   kicker="KEY IDEA"),
    pillars_title="Your Toolkit",
    pillars=[
        ("Build", ["Python 3.11+", "Claude Code or OpenAI Codex", "Git and GitHub"]),
        ("Data", ["Twelve Data", "Yahoo Finance (yfinance)", "Equibles", "Reddit API", "NewsAPI.org"]),
        ("Trade and show", ["Alpaca paper account", "Streamlit dashboard", "Offline sample data"]),
    ],
    arc_title="How Every Lab Progresses",
    arc=["Read the agent's spec and its message contract.",
         "Prompt your AI coding assistant with the lab prompt.",
         "Review the generated code against the spec.",
         "Run the lab's checks offline, then with your API keys.",
         "Commit to Git before the next agent."],
)

LAB_SHOTS = {}

# ------------------------------------------------------------------ LG content
LG_INTRO = ("This course teaches you to build a multi AI agents workflow for stock trading from scratch with AI vibe "
            "coding. You design eight cooperating agents - a lead agent that orchestrates finance research, news "
            "sentiment, trading strategy, signal generation, stock trading, performance analysis and strategy review - "
            "and you direct an AI coding assistant such as Claude Code or OpenAI Codex to write each one. You review "
            "the code against a written contract and prove it with tests before moving on.")
LG_INTRO2 = ("The finished project gathers Twelve Data candles at 1-minute, 15-minute and 1-hour intervals, Yahoo "
             "Finance and Equibles company data, and Reddit and NewsAPI sentiment; formulates a strategy from trend, "
             "momentum, volatility, VWAP, RSI and MACD; places long or short orders on an Alpaca paper account; "
             "reports its performance on a dashboard; and improves its own strategy through a review loop. You "
             "finish by pushing your project to your own GitHub repository. Everything runs offline on sample data "
             "too, so no lab is blocked by a missing key. All trading is paper trading; nothing here is investment advice.")
LG_SETUP = dict(
    needs=[
        "Prerequisite: complete AI Powered Quantitative Trading Fundamentals (C728) first - it demonstrates the multi AI agents trading system and the indicators, backtesting and paper trading this course builds on.",
        "A laptop (Windows, macOS or Linux) with Python 3.11 or later, Git and a code editor such as Visual Studio Code.",
        "An AI coding assistant: Claude Code or OpenAI Codex (either works; prompts are written for both).",
        "A free GitHub account.",
        "Optional free API keys for the live labs: Twelve Data, Equibles, NewsAPI.org, a Reddit 'script' app, and an Alpaca paper-trading account. Without them every lab runs on the bundled sample data.",
        "Optional: an Anthropic or OpenAI API key so the agents use an LLM brain; without it each agent uses its rule-based brain.",
    ],
    verify_text="Confirm your tools before Lab 1.",
    verify_code="$ python --version     # 3.11 or later\n$ git --version\n$ claude --version     # or: codex --version",
    conventions=[
        "Text in a grey box is either a prompt to paste into your AI coding assistant or a command to run in the terminal - the step says which.",
        "<YOUR-VALUE> placeholders are replaced with your own values. API keys go only in .env, never in code, prompts or screenshots.",
        "OFFLINE=true runs every agent on the bundled sample data and the simulated paper broker.",
    ],
)
LAB_NOTE = ("Use paper-trading accounts only. Keep API keys in .env (git-ignored). The sample data in this course is "
            "synthetic and for training only; nothing in this course is investment advice.")
LG_WRAPUP = dict(
    title="Wrap-Up",
    intro="You designed, vibe-coded, tested and published a self-improving multi AI agents trading workflow.",
    sections=[
        dict(title="What you built", bullets=[
            "Eight agents connected by a typed message contract and orchestrated by a lead agent.",
            "Live and offline data from Twelve Data, Yahoo Finance, Equibles, Reddit and NewsAPI.",
            "A strategy that mixes six algorithms with sentiment, long/short/null signals and automated Alpaca paper orders.",
            "A performance dashboard and a strategy review loop that changes the next run.",
        ]),
        dict(title="Keep it safe", bullets=[
            "Stay on paper until you understand every agent's behaviour and its failure modes.",
            "Never commit .env; rotate any key that has been pasted into a chat or a screenshot.",
            "Treat posts, headlines and model output as untrusted data, never as instructions.",
        ]),
    ],
)
LG_NEXT_STEPS = [
    "Run the workflow on a schedule during the US session and watch the review loop adjust the strategy.",
    "Add a risk-management agent (position limits, stop-loss, maximum daily loss) before ever considering real money.",
    "Swap the rule brains for an LLM brain and compare the decisions on the same data.",
    "Revisit the multi AI agents trading system demonstrated in AI Powered Quantitative Trading Fundamentals (C728) and compare it with the one you built.",
]
LG_GLOSSARY = [
    ("Agent", "A program with one role, its own instructions and data tools, that returns a structured result."),
    ("Lead agent", "The orchestrator that decides the order of work and summarises the run."),
    ("Message contract", "The agreed JSON structure each agent returns and the next agent reads."),
    ("AI vibe coding", "Building software by describing it to an AI coding assistant, then reviewing and testing what it writes."),
    ("Candle", "Open, high, low, close and volume for one time interval (1min, 15min, 1h)."),
    ("VWAP", "Volume-weighted average price; price above VWAP suggests buyers are in control."),
    ("RSI", "Relative Strength Index, 0-100; below 30 oversold, above 70 overbought."),
    ("MACD", "Moving-average convergence divergence; MACD above its signal line is bullish momentum."),
    ("Sentiment score", "A number from -1 (very negative) to +1 (very positive) summarising posts and headlines."),
    ("Long / short / null", "Buy to profit from a rise / sell short to profit from a fall / stay out."),
    ("Paper trading", "Simulated trading with virtual money on a real broker API."),
    ("Sharpe ratio", "Average return divided by its volatility, annualised; higher is better."),
    ("Maximum drawdown", "The largest peak-to-trough fall in equity."),
    ("Feedback loop", "The review agent's guidance changes how the strategy agent behaves on the next run."),
]
NEXT_STEPS = dict(title="Continuing Your Journey", items=[
    "Compare your agents with the multi AI agents system demonstrated in the prerequisite course C728.",
    "Add a risk-management agent and backtest the workflow before any live use.",
    "Schedule the lead agent to run every 15 minutes during the US session on paper.",
])
THANK_YOU = dict(body="You built a self-improving multi AI agents trading workflow from scratch and published it on GitHub.",
                 kicker="THANK YOU FOR ATTENDING")

# ------------------------------------------------------------------ version history
VERSION_HISTORY = [
    ("2.0", VERSION_DATE, "New course: Build a Multi AI Agents Workflow for Stock Trading - eight agents (lead, finance "
     "research, news sentiment, trading strategy, signal generation, stock trader, performance analysis, strategy "
     "review), built with AI vibe coding over eight labs; 9:30am - 5:30pm, 7.5 hours.", TRAINER),
]
