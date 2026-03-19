import pandas as pd
from data import fetch_prices


def run_backtest(prices: pd.DataFrame, initial_investment: float) -> pd.DataFrame:
    """
    Equal-weighted portfolio vs SPY benchmark.

    Returns a DataFrame with 'portfolio' and 'benchmark' columns,
    indexed by date.
    """
    # daily returns per ticker
    # equal weights -> weighted daily portfolio return
    # compound into dollar value starting at initial_investment
    # fetch SPY for same date range, align dates, do the same
    # return combined df
    pass
