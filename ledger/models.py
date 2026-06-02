from dataclasses import dataclass
from typing import Literal

import pandas as pd


RebalanceFrequency = Literal["none", "monthly", "quarterly", "annual"]


@dataclass(frozen=True)
class BacktestConfig:
    initial_investment: float
    weights: dict[str, float]
    benchmark_ticker: str = "SPY"
    rebalance_frequency: RebalanceFrequency = "none"


@dataclass(frozen=True)
class BacktestResult:
    values: pd.DataFrame
    allocation: pd.DataFrame
    assumptions: dict[str, str]

