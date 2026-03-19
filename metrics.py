import pandas as pd
import numpy as np


def total_return(portfolio: pd.Series) -> float:
    """Percentage gain from first to last value."""
    pass


def annualized_return(portfolio: pd.Series) -> float:
    """CAGR over the backtest period."""
    pass


def sharpe_ratio(portfolio: pd.Series, risk_free_rate: float = 0.04) -> float:
    """
    Risk-adjusted return. risk_free_rate is annual (default ~4%, roughly current T-bills).
    """
    pass


def max_drawdown(portfolio: pd.Series) -> float:
    """Largest peak-to-trough decline. Always <= 0."""
    pass


def summary(portfolio: pd.Series, risk_free_rate: float = 0.04) -> dict:
    # TODO: aggregate the four metrics above into a dict
    pass
