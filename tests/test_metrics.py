import numpy as np
import pandas as pd
import pytest

from metrics import annualized_return, max_drawdown, sharpe_ratio, total_return


def test_total_return():
    values = pd.Series([100, 125], index=pd.to_datetime(["2024-01-01", "2025-01-01"]))

    assert total_return(values) == pytest.approx(0.25)


def test_annualized_return():
    values = pd.Series([100, 121], index=pd.to_datetime(["2024-01-01", "2025-01-01"]))

    assert annualized_return(values) == pytest.approx(0.209, rel=0.01)


def test_sharpe_ratio_returns_nan_for_zero_volatility():
    values = pd.Series([100, 100, 100], index=pd.date_range("2024-01-01", periods=3))

    assert np.isnan(sharpe_ratio(values))


def test_max_drawdown():
    values = pd.Series([100, 120, 90, 110], index=pd.date_range("2024-01-01", periods=4))

    assert max_drawdown(values) == pytest.approx(-0.25)

