from __future__ import annotations

import numpy as np
import pandas as pd


def total_return(values: pd.Series) -> float:
    return (values.iloc[-1] / values.iloc[0]) - 1


def annualized_return(values: pd.Series) -> float:
    years = _years(values)
    if years <= 0:
        return np.nan

    return (1 + total_return(values)) ** (1 / years) - 1


def sharpe_ratio(values: pd.Series, risk_free_rate: float = 0.04) -> float:
    daily_returns = values.pct_change().dropna()
    if daily_returns.empty or daily_returns.std() == 0:
        return np.nan

    excess = daily_returns - (risk_free_rate / 252)
    return float((excess.mean() / excess.std()) * np.sqrt(252))


def max_drawdown(values: pd.Series) -> float:
    peak = values.cummax()
    drawdown = (values - peak) / peak
    return float(drawdown.min())


def summary(values: pd.Series, risk_free_rate: float = 0.04) -> dict[str, float]:
    return {
        "total_return": total_return(values),
        "annualized_return": annualized_return(values),
        "sharpe_ratio": sharpe_ratio(values, risk_free_rate),
        "max_drawdown": max_drawdown(values),
    }


def _years(values: pd.Series) -> float:
    days = (values.index[-1] - values.index[0]).days
    return days / 365.25
