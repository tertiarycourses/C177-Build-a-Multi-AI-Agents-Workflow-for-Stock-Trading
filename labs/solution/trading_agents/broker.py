"""Order execution: Alpaca PAPER trading (alpaca-py) or, offline, a simulated paper broker."""
from __future__ import annotations

from trading_agents import store
from trading_agents.config import settings

START_CASH = 100_000.0


class PaperSim:
    name = "paper-sim"

    def __init__(self):
        self.state = store.read("sim_account.json", {"cash": START_CASH, "positions": {}, "prices": {}})

    def _save(self):
        store.write("sim_account.json", self.state)

    def mark(self, symbol: str, price: float) -> None:
        self.state["prices"][symbol] = price
        self._save()

    def position(self, symbol: str) -> int:
        return int(self.state["positions"].get(symbol, {}).get("qty", 0))

    def positions(self) -> dict:
        return {k: v["qty"] for k, v in self.state["positions"].items() if v["qty"]}

    def equity(self) -> float:
        value = sum(v["qty"] * self.state["prices"].get(k, v["avg"]) for k, v in self.state["positions"].items())
        return round(self.state["cash"] + value, 2)

    def submit(self, symbol: str, side: str, qty: int, price: float) -> dict:
        pos = self.state["positions"].setdefault(symbol, {"qty": 0, "avg": price})
        signed = qty if side == "buy" else -qty
        realized = 0.0
        if pos["qty"] and (pos["qty"] > 0) != (signed > 0):          # closing (part of) the position
            closed = min(abs(signed), abs(pos["qty"]))
            realized = closed * (price - pos["avg"]) * (1 if pos["qty"] > 0 else -1)
        new_qty = pos["qty"] + signed
        if new_qty and (pos["qty"] == 0 or (pos["qty"] > 0) != (new_qty > 0)):
            pos["avg"] = price
        elif new_qty and (pos["qty"] > 0) == (signed > 0):
            pos["avg"] = (pos["avg"] * abs(pos["qty"]) + price * qty) / abs(new_qty)
        pos["qty"] = new_qty
        self.state["cash"] -= signed * price
        self.state["prices"][symbol] = price
        self._save()
        return {"status": "filled", "detail": f"{side} {qty} {symbol} @ {price:.2f}", "realized": round(realized, 2)}


class AlpacaPaper:
    name = "alpaca-paper"

    def __init__(self):
        from alpaca.trading.client import TradingClient
        s = settings()
        self.client = TradingClient(s.alpaca_key, s.alpaca_secret, paper=True)    # PAPER only

    def mark(self, symbol: str, price: float) -> None:
        pass

    def position(self, symbol: str) -> int:
        try:
            return int(float(self.client.get_open_position(symbol).qty))
        except Exception:
            return 0

    def positions(self) -> dict:
        return {p.symbol: int(float(p.qty)) for p in self.client.get_all_positions()}

    def equity(self) -> float:
        return float(self.client.get_account().equity)

    def submit(self, symbol: str, side: str, qty: int, price: float) -> dict:
        from alpaca.trading.enums import OrderSide, TimeInForce
        from alpaca.trading.requests import MarketOrderRequest
        req = MarketOrderRequest(symbol=symbol, qty=qty, side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
                                 time_in_force=TimeInForce.DAY)
        o = self.client.submit_order(req)
        return {"status": "submitted", "detail": f"Alpaca order {o.id} {side} {qty} {symbol} ({o.status})",
                "realized": 0.0}


def get_broker():
    s = settings()
    if not s.offline and s.alpaca_key and s.alpaca_secret:
        return AlpacaPaper()
    return PaperSim()
