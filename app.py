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
    # Split "AAPL, MSFT, GOOGL" into ["AAPL", "MSFT", "GOOGL"]
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    # --- Validate inputs ---
    if not tickers:
        st.error("Please enter at least one ticker.")
        st.stop()
    if start_date >= end_date:
        st.error("Start date must be before end date.")
        st.stop()
    if (end_date - start_date).days < 30:
        st.error("Date range must be at least 30 days.")
        st.stop()

    # --- Fetch prices ---
    # st.spinner shows a loading message while the block runs (like a progress indicator)
    with st.spinner("Fetching price data..."):
        try:
            prices, missing = fetch_prices(
                tickers,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
        except ValueError as e:
            st.error(f"Could not fetch data: {e}")
            st.stop()

    if missing:
        # warn but continue with the valid tickers
        st.warning(f"No data found for: {', '.join(missing)}. Continuing without them.")

    # --- Run backtest ---
    results = run_backtest(prices, initial_investment)

    # --- Compute metrics ---
    # summary() returns a dict like {"total_return": 0.42, "sharpe_ratio": 1.1, ...}
    portfolio_metrics = summary(results["portfolio"])
    benchmark_metrics = summary(results["benchmark"])

    # --- Chart ---
    st.subheader("Portfolio vs Benchmark (SPY)")
    st.line_chart(results, y=["portfolio", "benchmark"])

    # --- Metrics table ---
    st.subheader("Performance Metrics")

    # Build a table with one row per metric, two columns (portfolio vs benchmark)
    metrics_df = pd.DataFrame({
        "Portfolio": portfolio_metrics,
        "Benchmark (SPY)": benchmark_metrics,
    })

    # Format as percentages or plain numbers depending on the metric
    pct_rows = ["total_return", "annualized_return", "max_drawdown"]
    metrics_df.index.name = "Metric"

    def fmt(val, metric):
        if metric in pct_rows:
            return f"{val:.2%}"
        return f"{val:.2f}"

    # Apply formatting row by row
    formatted = metrics_df.copy().astype(str)
    for metric in metrics_df.index:
        for col in metrics_df.columns:
            formatted.loc[metric, col] = fmt(metrics_df.loc[metric, col], metric)

    st.dataframe(formatted, use_container_width=True)

else:
    st.info("Configure your portfolio in the sidebar and click **Run Backtest**.")
