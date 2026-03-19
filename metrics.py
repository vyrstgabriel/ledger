import pandas as pd
import numpy as np


def total_return(portfolio: pd.Series) -> float:
    """Percentage gain from first to last value."""
    return (portfolio.iloc[-1] / portfolio.iloc[0]) - 1


def annualized_return(portfolio: pd.Series) -> float:
    """CAGR over the backtest period."""
    days = (portfolio.index[-1] - portfolio.index[0]).days
    years = days / 365.25
    return (1 + total_return(portfolio)) ** (1 / years) - 1


def sharpe_ratio(portfolio: pd.Series, risk_free_rate: float = 0.04) -> float:
    """
    Risk-adjusted return. risk_free_rate is annual (default ~4%, roughly current T-bills).
    """
    daily_returns = portfolio.pct_change().dropna()
    excess = daily_returns - (risk_free_rate / 252)
    return (excess.mean() / excess.std()) * np.sqrt(252)


def max_drawdown(portfolio: pd.Series) -> float:
    """Largest peak-to-trough decline. Always <= 0."""
    peak = portfolio.cummax()
    drawdown = (portfolio - peak) / peak
    return drawdown.min()


def summary(portfolio: pd.Series, risk_free_rate: float = 0.04) -> dict:
    return {
        "total_return": total_return(portfolio),
        "annualized_return": annualized_return(portfolio),
        "sharpe_ratio": sharpe_ratio(portfolio, risk_free_rate),
        "max_drawdown": max_drawdown(portfolio)
    }
