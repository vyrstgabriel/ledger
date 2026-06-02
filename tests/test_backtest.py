import pandas as pd
import pytest

from backtest import run_backtest
from ledger.models import BacktestConfig


def test_buy_and_hold_compounds_weighted_asset_returns():
    dates = pd.date_range("2024-01-01", periods=3, freq="D")
    prices = pd.DataFrame(
        {
            "AAA": [100, 110, 121],
            "BBB": [100, 100, 100],
        },
        index=dates,
    )
    benchmark = pd.Series([100, 105, 110.25], index=dates, name="SPY")
    config = BacktestConfig(
        initial_investment=1000,
        weights={"AAA": 0.5, "BBB": 0.5},
        benchmark_ticker="SPY",
    )

    result = run_backtest(prices, benchmark, config)

    assert result.values["portfolio"].iloc[0] == pytest.approx(1000)
    assert result.values["portfolio"].iloc[-1] == pytest.approx(1105)
    assert result.values["benchmark"].iloc[-1] == pytest.approx(1102.5)


def test_rebalanced_portfolio_resets_to_target_weights_each_period():
    dates = pd.to_datetime(["2024-01-31", "2024-02-01", "2024-02-02"])
    prices = pd.DataFrame(
        {
            "AAA": [100, 200, 200],
            "BBB": [100, 100, 110],
        },
        index=dates,
    )
    benchmark = pd.Series([100, 100, 100], index=dates, name="SPY")
    config = BacktestConfig(
        initial_investment=1000,
        weights={"AAA": 0.5, "BBB": 0.5},
        benchmark_ticker="SPY",
        rebalance_frequency="monthly",
    )

    result = run_backtest(prices, benchmark, config)

    assert result.allocation.loc[dates[1], "AAA"] == pytest.approx(2 / 3)
    assert result.values["portfolio"].iloc[-1] == pytest.approx(1550)


def test_missing_weight_is_rejected():
    dates = pd.date_range("2024-01-01", periods=2, freq="D")
    prices = pd.DataFrame({"AAA": [100, 101], "BBB": [100, 101]}, index=dates)
    benchmark = pd.Series([100, 101], index=dates, name="SPY")
    config = BacktestConfig(initial_investment=1000, weights={"AAA": 1})

    with pytest.raises(ValueError, match="Missing weights"):
        run_backtest(prices, benchmark, config)
