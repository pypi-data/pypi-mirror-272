from typing import TypeVar

import numpy as np
import pandas as pd

from .stats import compsum

T = TypeVar("T", pd.Series, pd.DataFrame)

def __fill_first_value_with_zero(series: pd.Series) -> pd.Series:
    series.iloc[0] = 0.0
    return series

def to_log_returns(data: T) -> T:
    return np.log1p(to_returns(data))


def to_returns(data: T) -> T:
    if isinstance(data, pd.DataFrame):
        return data.apply(to_returns)
    if data.min() < 0:
        return __fill_first_value_with_zero(data.diff() / data.shift(1).abs())
    return __fill_first_value_with_zero(data / data.shift(1) - 1)




TPandas = TypeVar("TPandas", pd.DataFrame, pd.Series)


def to_prices(returns: pd.Series, base=1.0) -> pd.Series:
    """Arithcmetic returns to price series"""
    returns = returns.copy().fillna(0).replace([np.inf, -np.inf], float("NaN"))
    return base + base * compsum(returns)
