from __future__ import annotations

import pandas as pd

from ledger.models import BacktestConfig, BacktestResult


def run_backtest(
    prices: pd.DataFrame,
    benchmark_prices: pd.Series,
    config: BacktestConfig,
) -> BacktestResult:
    """
    Simulate a long-only portfolio against a supplied benchmark series.

    The function is intentionally pure: callers fetch data, choose benchmark
    symbols, and define assumptions before invoking the simulation.
    """
    prices = _clean_prices(prices)
    benchmark_prices = _clean_benchmark(benchmark_prices)
    weights = _weights_for_columns(config.weights, prices.columns)

    asset_returns = prices.pct_change().fillna(0)
    portfolio_returns, allocation = _portfolio_returns(
        asset_returns,
        weights,
        config.rebalance_frequency,
    )
    portfolio_values = config.initial_investment * (1 + portfolio_returns).cumprod()

    benchmark = benchmark_prices.reindex(portfolio_values.index).ffill().bfill()
    benchmark_returns = benchmark.pct_change().fillna(0)
    benchmark_values = config.initial_investment * (1 + benchmark_returns).cumprod()

    values = pd.DataFrame(
        {
            "portfolio": portfolio_values,
            "benchmark": benchmark_values,
        }
    )

    assumptions = {
        "price_source": "Adjusted close prices",
        "fees": "No transaction fees",
        "taxes": "No taxes",
        "cash": "Fully invested",
        "benchmark": config.benchmark_ticker,
        "rebalancing": config.rebalance_frequency,
    }

    return BacktestResult(values=values, allocation=allocation, assumptions=assumptions)


def _clean_prices(prices: pd.DataFrame) -> pd.DataFrame:
    if prices.empty:
        raise ValueError("Price data is empty.")

    cleaned = prices.sort_index().ffill().dropna(axis=1, how="any")
    if cleaned.empty:
        raise ValueError("No assets have complete price data for the selected range.")

    return cleaned


def _clean_benchmark(benchmark_prices: pd.Series) -> pd.Series:
    if benchmark_prices.empty:
        raise ValueError("Benchmark price data is empty.")

    return benchmark_prices.sort_index().ffill().dropna()


def _weights_for_columns(weights: dict[str, float], columns: pd.Index) -> pd.Series:
    normalized = pd.Series(weights, dtype=float).reindex(columns)
    if normalized.isna().any():
        missing = normalized[normalized.isna()].index.tolist()
        raise ValueError(f"Missing weights for: {', '.join(missing)}.")

    total = normalized.sum()
    if total <= 0:
        raise ValueError("Weights must sum to a positive number.")

    return normalized / total


def _portfolio_returns(
    asset_returns: pd.DataFrame,
    target_weights: pd.Series,
    rebalance_frequency: str,
) -> tuple[pd.Series, pd.DataFrame]:
    if rebalance_frequency == "none":
        return _buy_and_hold_returns(asset_returns, target_weights)

    return _rebalanced_returns(asset_returns, target_weights, rebalance_frequency)


def _buy_and_hold_returns(
    asset_returns: pd.DataFrame,
    target_weights: pd.Series,
) -> tuple[pd.Series, pd.DataFrame]:
    asset_growth = (1 + asset_returns).cumprod()
    weighted_values = asset_growth.mul(target_weights, axis=1)
    portfolio_value = weighted_values.sum(axis=1)
    allocation = weighted_values.div(portfolio_value, axis=0)
    returns = portfolio_value.pct_change().fillna(0)
    return returns, allocation


def _rebalanced_returns(
    asset_returns: pd.DataFrame,
    target_weights: pd.Series,
    rebalance_frequency: str,
) -> tuple[pd.Series, pd.DataFrame]:
    periods = _rebalance_periods(asset_returns.index, rebalance_frequency)
    current_weights = target_weights.copy()
    returns = []
    allocations = []
    previous_period = None

    for date, row in asset_returns.iterrows():
        current_period = periods.loc[date]
        if previous_period is not None and current_period != previous_period:
            current_weights = target_weights.copy()

        day_return = float((current_weights * row).sum())
        end_weights = current_weights * (1 + row)
        if end_weights.sum() != 0:
            end_weights = end_weights / end_weights.sum()

        returns.append(day_return)
        allocations.append(end_weights)
        current_weights = end_weights
        previous_period = current_period

    return (
        pd.Series(returns, index=asset_returns.index, name="portfolio_return"),
        pd.DataFrame(allocations, index=asset_returns.index, columns=asset_returns.columns),
    )


def _rebalance_periods(index: pd.DatetimeIndex, frequency: str) -> pd.Series:
    frequency_map = {
        "monthly": "M",
        "quarterly": "Q",
        "annual": "Y",
    }
    if frequency not in frequency_map:
        raise ValueError(f"Unsupported rebalance frequency: {frequency}")

    return pd.Series(index.to_period(frequency_map[frequency]), index=index)
