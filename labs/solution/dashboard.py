"""Performance dashboard:  streamlit run dashboard.py"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from trading_agents import store
from trading_agents.agents import lead

st.set_page_config(page_title="Multi AI Agents Trading Desk", layout="wide")
st.title("Multi AI Agents Trading Desk")

symbols = st.text_input("Symbols", "NVDA, AAPL, SPY")
if st.button("Run the workflow"):
    res = lead.run([s.strip() for s in symbols.split(",") if s.strip()])
    st.success(res["summary"])
    st.subheader("Agent trace")
    st.dataframe(pd.DataFrame([{"agent": t["agent"], "brain": t["brain"]} for t in res["trace"]]))
    st.subheader("Signals and orders")
    st.dataframe(pd.DataFrame(res["orders"]))

perf = store.read("performance.json", {})
if perf:
    st.subheader("Performance (Performance Analysis Agent)")
    c = st.columns(5)
    c[0].metric("Equity", f"{perf['equity']:,.0f}")
    c[1].metric("Total return", f"{perf['total_return_pct']}%")
    c[2].metric("Sharpe", perf["sharpe"])
    c[3].metric("Max drawdown", f"{perf['max_drawdown_pct']}%")
    c[4].metric("Win rate", f"{perf['win_rate_pct']}%")
    curve = pd.DataFrame(store.rows("equity.jsonl"))
    if not curve.empty:
        st.line_chart(curve.set_index("at")["equity"])
guide = store.read("guidance.json", {})
if guide:
    st.subheader("Strategy guidance (Strategy Review Agent)")
    st.json(guide)
