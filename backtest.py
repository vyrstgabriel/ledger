import pandas as pd
from data import fetch_prices


def run_backtest(prices: pd.DataFrame, initial_investment: float) -> pd.DataFrame:
    """
    Equal-weighted portfolio vs SPY benchmark.

    Returns a DataFrame with 'portfolio' and 'benchmark' columns,
    indexed by date.
    """
    # daily returns per ticker
    daily_returns = prices.pct_change().dropna()

    # equalize weights
    weights = 1 / len(prices.columns)

    # weighted portfolio return per day
    portfolio_return = daily_returns.mul(weights).sum(axis=1)

    # compound into dollar value
    portfolio_values = initial_investment * (1 + portfolio_return).cumprod()

    # fetch SPY for same date range
    start = prices.index[0].strftime("%Y-%m-%d")
    end = prices.index[-1].strftime("%Y-%m-%d")
    spy_prices, _ = fetch_prices(["SPY"], start, end)

    # align SPY to portfolio dates
    spy_prices = spy_prices.reindex(portfolio_values.index).ffill()

    # SPY daily returns and dollar value
    spy_returns = spy_prices["SPY"].pct_change().fillna(0)
    benchmark_values = initial_investment * (1 + spy_returns).cumprod()

    return pd.DataFrame({
        "portfolio": portfolio_values,
        "benchmark": benchmark_values,
    })
