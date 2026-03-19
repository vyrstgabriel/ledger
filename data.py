import yfinance as yf
import pandas as pd


def fetch_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Fetch adjusted closing prices for a list of tickers over a date range.

    Args:
        tickers: List of stock ticker symbols, e.g. ["AAPL", "MSFT", "SPY"]
        start:   Start date as "YYYY-MM-DD"
        end:     End date as "YYYY-MM-DD"

    Returns:
        DataFrame with dates as index and tickers as columns.
        Columns with no data (bad tickers) are dropped.
        Raises ValueError if no valid data is returned.
    """
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)

    if raw.empty:
        raise ValueError(f"No price data returned for tickers: {tickers}")

    prices = raw["Close"]

    # yfinance returns a Series (not DataFrame) when only one ticker is given
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    # Ensure columns match requested tickers (in case some returned no data)
    prices = prices.reindex(columns=tickers)
    missing = prices.columns[prices.isna().all()].tolist()
    if missing:
        prices = prices.drop(columns=missing)

    if prices.empty or len(prices.columns) == 0:
        raise ValueError(f"No valid data returned for any ticker: {tickers}")

    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "Date"

    return prices, missing
