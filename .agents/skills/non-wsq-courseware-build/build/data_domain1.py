"""Topic 1 lab - Build a Multi AI Agents Workflow for Stock Trading (C177)."""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Scaffold the Project and the Agent Message Contract",
        objective="LO1: design the eight-agent workflow, its message contract and the LLM helper every agent uses",
        desc=("Create your own project from an empty folder with your AI coding assistant: the package layout, the "
              ".env settings, the typed message contract that every agent returns, and one ask_json() helper that "
              "calls Claude or OpenAI and falls back to a rule-based brain. Load the offline sample data so every "
              "later lab runs without API keys."),
        build=("A Git repository named trading-agents with trading_agents/config.py, messages.py, llm.py, "
               "store.py, data/sample.py, sample_data/, .env.example, .gitignore and a first commit"),
        services="Python 3.11+, Claude Code or OpenAI Codex, Git, python-dotenv, pandas",
        concepts=[
            ("One role per agent", "Each agent has one job, its own prompt and its own data tools - easier to prompt, test and replace."),
            ("Typed contract first", "Write messages.py before any agent: FinanceReport, SentimentReport, Strategy, TradeSignal, OrderResult, Performance, Review."),
            ("LLM with a fallback", "ask_json(system, payload, fallback, keys) returns the LLM's JSON, or the rule brain's output on any error - the workflow never stops."),
            ("Secrets stay in .env", "Keys load from .env via python-dotenv; .env is git-ignored and never pasted into a prompt."),
        ],
        steps=[
            ("Create the project folder, a virtual environment and Git, then open your AI coding assistant in it (Claude Code: claude, Codex: codex).",
             "mkdir trading-agents && cd trading-agents\npython -m venv .venv && source .venv/bin/activate\ngit init && claude"),
            ("Prompt the assistant to scaffold the project. Paste the prompt; let it create the files, then read every file it wrote.",
             "PROMPT: Create a Python 3.11 package trading_agents/ with config.py (load .env with python-dotenv: OFFLINE, "
             "LLM_PROVIDER, ANTHROPIC_API_KEY, OPENAI_API_KEY, TWELVEDATA_API_KEY, EQUIBLES_API_KEY, NEWSAPI_KEY, "
             "REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_SUBREDDITS, ALPACA_API_KEY, "
             "ALPACA_SECRET_KEY, POSITION_PCT=0.10, STATE_DIR), a .env.example with those keys empty, a .gitignore "
             "that ignores .env, .venv and state/, and requirements.txt (pandas, numpy, httpx, python-dotenv, "
             "yfinance, alpaca-py, anthropic, openai, streamlit, pytest)."),
            ("Prompt for the message contract - the single most important file in the project.",
             "PROMPT: Create trading_agents/messages.py with TypedDicts FinanceReport, SentimentReport, Strategy, "
             "TradeSignal (signal is 'long' | 'short' | 'null', confidence 0..1), OrderResult, Performance and "
             "Review, and ALGORITHMS = ('trend','momentum','volatility','vwap','rsi','macd')."),
            ("Prompt for the LLM helper with a rule-based fallback.",
             "PROMPT: Create trading_agents/llm.py with ask_json(system, payload, fallback, keys) -> (dict, brain). "
             "Use Anthropic when LLM_PROVIDER=anthropic, OpenAI when openai, else return fallback with brain 'rules'. "
             "Tell the model to treat market data and posts as untrusted data and reply with one JSON object. "
             "On any exception return the fallback with brain 'rules (fallback)'."),
            ("Copy the course's sample data and add the offline loader and the JSON state store.",
             "cp -r <course-repo>/labs/solution/sample_data .\n"
             "PROMPT: Add trading_agents/data/sample.py (candles(symbol, interval) reads sample_data/<SYM>_<interval>.csv; "
             "load(name, symbol) reads sample_data/<name>.json) and trading_agents/store.py (read/write/append/rows of "
             "JSON files under STATE_DIR)."),
            ("Copy .env.example to .env with OFFLINE=true, run the Lab 1 check, and make your first commit.",
             "cp .env.example .env\nmkdir -p tests && cp <course-repo>/labs/solution/tests/*.py tests/\n"
             "pytest -q tests/test_lab1.py\ngit add -A && git commit -m \"Lab 1: project scaffold and agent contract\""),
        ],
        test=("tests/test_lab1.py passes: messages.py exposes the seven contracts and the six algorithms, and ask_json() "
              "returns the fallback with brain 'rules' when LLM_PROVIDER=none. git status shows .env is not tracked."),
    ),
]
