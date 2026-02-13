#!/usr/bin/env python
# coding: utf-8

# In[5]:


from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple, Union

import pandas as pd
import yfinance as yf

StrategyFn = Callable[[pd.Series, pd.DataFrame, dict], pd.Series]


@dataclass
class BacktestResult:
    prices: pd.Series
    returns: pd.Series
    position: pd.Series
    trades: pd.Series
    equity_strategy: pd.Series
    equity_buyhold: pd.Series
    drawdown: pd.Series
    results: Dict[str, Union[str, float, int]]


def load_prices(
    ticker: str,
    start: str,
    end: Optional[str] = None,
    auto_adjust: bool = True
) -> Tuple[pd.Series, pd.DataFrame]:
    data = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=auto_adjust,
        progress=False
    )
    if data.empty:
        raise ValueError(f"No data returned for {ticker}")

    close = data["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    prices = close.dropna().astype(float)
    data = data.loc[prices.index]
    return prices, data


def run_backtest(
    ticker: str,
    start: str,
    strategy_fn: StrategyFn,
    strategy_params: Optional[dict] = None,
    end: Optional[str] = None,
    initial_capital: float = 1_000_000.0,
    fee_rate_per_trade: float = 0.0005,
    shift_signals_by: int = 1,
    auto_adjust: bool = True,
) -> BacktestResult:
    params = strategy_params or {}

    prices, data = load_prices(ticker, start=start, end=end, auto_adjust=auto_adjust)

    raw_position = strategy_fn(prices, data, params)
    raw_position = raw_position.reindex(prices.index).fillna(0.0)
    raw_position = pd.to_numeric(raw_position, errors="coerce").fillna(0.0)

    position = raw_position.shift(shift_signals_by).fillna(0.0)

    returns = prices.pct_change().fillna(0.0)
    trades = position.diff().abs().fillna(0.0)

    strategy_returns_gross = position * returns
    strategy_returns_net = strategy_returns_gross - trades * fee_rate_per_trade

    equity_strategy = initial_capital * (1.0 + strategy_returns_net).cumprod()
    equity_buyhold = initial_capital * (prices / prices.iloc[0])

    running_max = equity_strategy.cummax()
    drawdown = equity_strategy / running_max - 1.0
    max_drawdown = float(drawdown.min())

    final_value = float(equity_strategy.iloc[-1])
    profit = final_value - initial_capital
    profit_pct = final_value / initial_capital - 1.0

    results = {
        "ticker": ticker,
        "start": start,
        "end": str(equity_strategy.index[-1].date()),
        "initial_capital": float(initial_capital),
        "ending_value_strategy": float(equity_strategy.iloc[-1]),
        "ending_value_buyhold": float(equity_buyhold.iloc[-1]),
        "profit_strategy": float(profit),
        "profit_pct_strategy": float(profit_pct),
        "max_drawdown_strategy": float(max_drawdown),
        "trades": float(trades.sum()),
        "fee_rate_per_trade": float(fee_rate_per_trade),
        "strategy_name": getattr(strategy_fn, "__name__", "strategy_fn"),
        "strategy_params": dict(params),
    }

    return BacktestResult(
        prices=prices,
        returns=returns,
        position=position,
        trades=trades,
        equity_strategy=equity_strategy,
        equity_buyhold=equity_buyhold,
        drawdown=drawdown,
        results=results,
    )


