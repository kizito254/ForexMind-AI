from __future__ import annotations

from itertools import product

from .backtester import run_backtest, strategy_with_params
from .models import BacktestRequest, OptimizationRequest, OptimizationResponse, StrategyRequest
from .strategy_generator import generate_strategy


def optimize_strategy(payload: OptimizationRequest) -> OptimizationResponse:
    base = generate_strategy(
        StrategyRequest(pair=payload.pair, timeframe=payload.timeframe, risk_tolerance="medium")
    )

    best_strategy = base
    best_result = None
    tried = 0

    for rsi_buy, rsi_sell, ema in product(payload.rsi_buy_values, payload.rsi_sell_values, payload.ema_values):
        if rsi_buy >= rsi_sell:
            continue
        candidate = strategy_with_params(base, rsi_buy, rsi_sell, ema)
        result = run_backtest(
            BacktestRequest(
                strategy=candidate,
                candles=payload.candles,
                initial_balance=payload.initial_balance,
            )
        )
        tried += 1
        if best_result is None or result.metrics.total_return_pct > best_result.metrics.total_return_pct:
            best_result = result
            best_strategy = candidate

    if best_result is None:
        best_result = run_backtest(
            BacktestRequest(strategy=best_strategy, candles=payload.candles, initial_balance=payload.initial_balance)
        )

    return OptimizationResponse(
        best_strategy=best_strategy,
        best_metrics=best_result.metrics,
        tried_combinations=tried,
    )
