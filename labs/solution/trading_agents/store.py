"""Tiny JSON state store: runs, trades, equity curve, strategy guidance and the latest performance."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from trading_agents.config import settings


def _path(name: str):
    d = settings().state_dir
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read(name: str, default):
    p = _path(name)
    return json.loads(p.read_text()) if p.exists() else default


def write(name: str, value) -> None:
    _path(name).write_text(json.dumps(value, indent=2, default=str))


def append(name: str, row: dict) -> None:
    with _path(name).open("a") as f:
        f.write(json.dumps({"at": now(), **row}, default=str) + "\n")


def rows(name: str) -> list[dict]:
    p = _path(name)
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []
