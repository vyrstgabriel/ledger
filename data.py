import yfinance as yf
import pandas as pd


def fetch_prices(tickers: list[str], start: str, end: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Fetch adjusted closing prices for a list of tickers over a date range.

    Args:
        tickers: List of stock ticker symbols, e.g. ["AAPL", "MSFT", "SPY"]
        start:   Start date as "YYYY-MM-DD"
        end:     End date as "YYYY-MM-DD"

    Returns:
        Tuple of (prices, missing_tickers). Prices has dates as index and tickers as columns.
        Columns with no data (bad tickers) are dropped.
        Raises ValueError if no valid data is returned.
    """
    # one ticker at a time to avoid yfinance batch drop bug
    frames = {}
    missing = []
    for ticker in tickers:
        raw = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=True,
            progress=False,
            multi_level_index=False,
        )
        # Retry once because yfinance can occasionally return an empty first response.
        if raw.empty or "Close" not in raw.columns:
            raw = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=True,
                progress=False,
                multi_level_index=False,
            )
        if raw.empty or "Close" not in raw.columns:
            missing.append(ticker)
        else:
            frames[ticker] = raw["Close"].squeeze()

    if not frames:
        raise ValueError(f"No valid data returned for any ticker: {tickers}")

    prices = pd.DataFrame(frames)
    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "Date"

    return prices, missing
