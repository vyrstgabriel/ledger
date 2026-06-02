# Ledger

A portfolio backtesting tool built with Streamlit. Enter stock tickers, optional target weights, a benchmark, a date range, and a rebalancing policy to compare portfolio performance against a market benchmark.

## Features

- Fetches adjusted closing prices via Yahoo Finance
- Supports equal-weighted and custom-weighted portfolios
- Supports buy-and-hold, monthly, quarterly, and annual rebalancing
- Lets users choose the benchmark ticker
- Reports total return, annualized return, Sharpe ratio, and max drawdown
- Shows equity curve, allocation drift, and explicit backtest assumptions
- Includes tests for the core backtest and metric calculations

## Run locally

```bash
git clone https://github.com/your-username/ledger.git
cd ledger
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
python -m pytest
```

## Project structure

| File | Responsibility |
|---|---|
| `app.py` | Streamlit UI, input validation, chart and metrics display |
| `data.py` | Fetches adjusted closing prices from Yahoo Finance via yfinance |
| `backtest.py` | Pure portfolio simulation and benchmark comparison |
| `metrics.py` | Calculates total return, annualized return, Sharpe ratio, max drawdown |
| `ledger/models.py` | Typed configuration and result objects |
| `ledger/validation.py` | Input parsing and portfolio weight validation |
| `tests/` | Regression tests for calculations |

## Backtest assumptions

- Uses adjusted close prices
- Assumes a long-only, fully invested portfolio
- Does not model taxes, fees, spreads, or slippage
- Uses the selected risk-free rate for Sharpe ratio calculations
- Normalizes weights across assets that return usable market data
