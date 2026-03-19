# Ledger

**Live app: [ledger.streamlit.app] *placeholder*

A portfolio backtesting tool built with Streamlit. Enter any set of stock tickers, a date range, and an initial investment amount to see how an equal-weighted portfolio would have performed against the SPY benchmark.

## Features

- Fetches adjusted closing prices via Yahoo Finance
- Equal-weighted portfolio simulation
- SPY benchmark comparison
- Performance metrics: total return, annualized return, Sharpe ratio, max drawdown
- Dark-themed interactive chart

## Run locally

```bash
git clone https://github.com/your-username/ledger.git
cd ledger
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

| File | Responsibility |
|---|---|
| `app.py` | Streamlit UI, input validation, chart and metrics display |
| `data.py` | Fetches adjusted closing prices from Yahoo Finance via yfinance |
| `backtest.py` | Computes daily portfolio and benchmark values from price data |
| `metrics.py` | Calculates total return, annualized return, Sharpe ratio, max drawdown |
