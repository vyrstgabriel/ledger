import streamlit as st
import pandas as pd
from datetime import date

from data import fetch_prices
from backtest import run_backtest
from metrics import summary


st.set_page_config(page_title="Ledger", layout="wide")
st.title("Ledger")
st.caption("Equal-weighted portfolio backtester vs SPY benchmark")

# --- Sidebar inputs ---
with st.sidebar:
    st.header("Configuration")
    tickers_input = st.text_input(
        "Tickers (comma-separated)",
        value="AAPL, MSFT, GOOGL",
    )
    start_date = st.date_input("Start date", value=pd.Timestamp("2020-01-01"))
    end_date = st.date_input("End date", value=pd.Timestamp("2024-12-31"))
    initial_investment = st.number_input(
        "Initial investment ($)", min_value=100.0, value=10000.0, step=100.0
    )
    run = st.button("Run Backtest", type="primary")

# --- Main panel ---
if run:
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    # TODO: validate inputs (empty tickers, bad dates, range too short)

    # TODO: fetch prices, handle bad tickers gracefully

    # TODO: run backtest

    # TODO: compute metrics for portfolio + benchmark

    # TODO: plot portfolio vs benchmark (Plotly)

    # TODO: metrics table below the chart

    st.info("Backend not yet implemented.")

else:
    st.info("Configure your portfolio in the sidebar and click **Run Backtest**.")
