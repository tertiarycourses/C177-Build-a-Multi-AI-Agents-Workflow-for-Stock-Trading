"""Settings from the environment (.env). Keys are read here only - never logged or sent to an LLM."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


@dataclass
class Settings:
    offline: bool = field(default_factory=lambda: _bool("OFFLINE", True))
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "none").lower())
    anthropic_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"))
    openai_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-5-mini"))
    twelvedata_key: str = field(default_factory=lambda: os.getenv("TWELVEDATA_API_KEY", ""))
    equibles_key: str = field(default_factory=lambda: os.getenv("EQUIBLES_API_KEY", ""))
    newsapi_key: str = field(default_factory=lambda: os.getenv("NEWSAPI_KEY", ""))
    reddit_id: str = field(default_factory=lambda: os.getenv("REDDIT_CLIENT_ID", ""))
    reddit_secret: str = field(default_factory=lambda: os.getenv("REDDIT_CLIENT_SECRET", ""))
    reddit_agent: str = field(default_factory=lambda: os.getenv("REDDIT_USER_AGENT", "trading-agents/1.0"))
    reddit_subs: str = field(default_factory=lambda: os.getenv("REDDIT_SUBREDDITS", "stocks,wallstreetbets,investing"))
    alpaca_key: str = field(default_factory=lambda: os.getenv("ALPACA_API_KEY", ""))
    alpaca_secret: str = field(default_factory=lambda: os.getenv("ALPACA_SECRET_KEY", ""))
    position_pct: float = field(default_factory=lambda: float(os.getenv("POSITION_PCT", "0.10")))
    state_dir: Path = field(default_factory=lambda: Path(os.getenv("STATE_DIR", str(ROOT / "state"))))
    sample_dir: Path = ROOT / "sample_data"


def settings() -> Settings:
    return Settings()
