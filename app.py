import pandas as pd
import streamlit as st

from backtest import run_backtest
from data import fetch_prices
from ledger.models import BacktestConfig
from ledger.validation import parse_tickers, parse_weights
from metrics import summary


st.set_page_config(page_title="Ledger", layout="wide")
st.title("Ledger")
st.caption("Portfolio backtesting with explicit assumptions")

REBALANCE_OPTIONS = {
    "Buy and hold": "none",
    "Monthly": "monthly",
    "Quarterly": "quarterly",
    "Annual": "annual",
}


def format_metric(value: float, metric: str) -> str:
    if pd.isna(value):
        return "N/A"
    if metric in {"total_return", "annualized_return", "max_drawdown"}:
        return f"{value:.2%}"
    return f"{value:.2f}"


with st.sidebar:
    st.header("Configuration")
    tickers_input = st.text_input("Tickers", value="AAPL, MSFT, GOOGL")
    weights_input = st.text_input(
        "Weights",
        value="",
        placeholder="Optional: AAPL:40, MSFT:35, GOOGL:25",
        help="Leave blank for equal weights. Custom weights must add up to 100.",
    )
    benchmark_ticker = st.text_input("Benchmark", value="SPY").strip().upper()
    start_date = st.date_input("Start date", value=pd.Timestamp("2020-01-01"))
    end_date = st.date_input("End date", value=pd.Timestamp("2024-12-31"))
    initial_investment = st.number_input(
        "Initial investment ($)",
        min_value=100.0,
        value=10000.0,
        step=100.0,
    )
    rebalance_label = st.selectbox("Rebalancing", list(REBALANCE_OPTIONS))
    risk_free_rate = st.number_input(
        "Risk-free rate (%)",
        min_value=0.0,
        value=4.0,
        step=0.25,
    ) / 100
    run = st.button("Run Backtest", type="primary")


if not run:
    st.info("Configure a portfolio in the sidebar and click **Run Backtest**.")
    st.stop()

try:
    tickers = parse_tickers(tickers_input)
    if not tickers:
        raise ValueError("Please enter at least one ticker.")
    if not benchmark_ticker:
        raise ValueError("Please enter a benchmark ticker.")
    if start_date >= end_date:
        raise ValueError("Start date must be before end date.")
    if (end_date - start_date).days < 30:
        raise ValueError("Date range must be at least 30 days.")

    weights = parse_weights(weights_input, tickers)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

start = start_date.strftime("%Y-%m-%d")
end = end_date.strftime("%Y-%m-%d")

with st.spinner("Fetching price data..."):
    try:
        prices, missing = fetch_prices(tickers, start, end)
        benchmark_prices, benchmark_missing = fetch_prices([benchmark_ticker], start, end)
    except ValueError as exc:
        st.error(f"Could not fetch data: {exc}")
        st.stop()

if missing:
    st.warning(f"No data found for: {', '.join(missing)}. Continuing without them.")
if benchmark_missing:
    st.error(f"No data found for benchmark: {benchmark_ticker}.")
    st.stop()

active_weights = {ticker: weights[ticker] for ticker in prices.columns if ticker in weights}
if not active_weights:
    st.error("None of the requested portfolio tickers returned usable data.")
    st.stop()

config = BacktestConfig(
    initial_investment=initial_investment,
    weights=active_weights,
    benchmark_ticker=benchmark_ticker,
    rebalance_frequency=REBALANCE_OPTIONS[rebalance_label],
)

try:
    result = run_backtest(prices, benchmark_prices[benchmark_ticker], config)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

portfolio_metrics = summary(result.values["portfolio"], risk_free_rate)
benchmark_metrics = summary(result.values["benchmark"], risk_free_rate)

metric_columns = st.columns(4)
for column, metric in zip(metric_columns, portfolio_metrics):
    column.metric(metric.replace("_", " ").title(), format_metric(portfolio_metrics[metric], metric))

st.subheader(f"Portfolio vs {benchmark_ticker}")
st.line_chart(result.values, y=["portfolio", "benchmark"])

left, right = st.columns([2, 1])

with left:
    st.subheader("Performance Metrics")
    metrics_df = pd.DataFrame(
        {
            "Portfolio": portfolio_metrics,
            benchmark_ticker: benchmark_metrics,
        }
    )
    formatted = metrics_df.copy().astype(str)
    for metric in metrics_df.index:
        for column in metrics_df.columns:
            formatted.loc[metric, column] = format_metric(metrics_df.loc[metric, column], metric)
    formatted.index = formatted.index.str.replace("_", " ").str.title()
    st.dataframe(formatted, use_container_width=True)

with right:
    st.subheader("Assumptions")
    assumptions = pd.DataFrame(
        result.assumptions.items(),
        columns=["Assumption", "Value"],
    )
    st.dataframe(assumptions, hide_index=True, use_container_width=True)

st.subheader("Allocation Drift")
st.line_chart(result.allocation)

