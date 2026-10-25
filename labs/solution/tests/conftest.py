import pytest


@pytest.fixture(autouse=True)
def offline(tmp_path, monkeypatch):
    monkeypatch.setenv("OFFLINE", "true")
    monkeypatch.setenv("LLM_PROVIDER", "none")
    monkeypatch.setenv("STATE_DIR", str(tmp_path / "state"))
