from __future__ import annotations

import math

import numpy as np
import pandas as pd
from fastapi import HTTPException

from .charting import write_equity_curve_image

from .models import BacktestMetrics, BacktestRequest, BacktestResponse, StrategyDefinition


def _rsi(series: pd.Series, period: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _prepare_dataframe(request: BacktestRequest) -> pd.DataFrame:
    if len(request.candles) < 30:
        raise HTTPException(status_code=422, detail="At least 30 candles are required for backtesting.")

    df = pd.DataFrame([c.model_dump() for c in request.candles]).sort_values("timestamp")
    if df["close"].isna().any() or (df["close"] <= 0).any():
        raise HTTPException(status_code=422, detail="Candle close prices must be positive and non-null.")

    df["rsi"] = _rsi(df["close"], request.strategy.rsi_period)
    df["ema"] = df["close"].ewm(span=request.strategy.ema_period, adjust=False).mean()
    prepared = df.dropna().reset_index(drop=True)
    if prepared.empty:
        raise HTTPException(status_code=422, detail="Insufficient valid data after indicator warm-up.")
    return prepared
    df = pd.DataFrame([c.model_dump() for c in request.candles]).sort_values("timestamp")
    df["rsi"] = _rsi(df["close"], request.strategy.rsi_period)
    df["ema"] = df["close"].ewm(span=request.strategy.ema_period, adjust=False).mean()
    return df.dropna().reset_index(drop=True)


def run_backtest(request: BacktestRequest) -> BacktestResponse:
    df = _prepare_dataframe(request)
    strategy = request.strategy

    balance = float(request.initial_balance)
    balance = request.initial_balance
    equity_curve = [balance]
    in_position = False
    entry_price = 0.0
    wins = 0
    losses = 0
    gross_profit = 0.0
    gross_loss = 0.0

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        bullish_cross = prev["close"] <= prev["ema"] and row["close"] > row["ema"]
        buy_signal = row["rsi"] < strategy.rsi_buy_threshold and bullish_cross

        if not in_position and buy_signal:
            in_position = True
            entry_price = float(row["close"])
            continue

        if in_position:
            pnl_pct = ((float(row["close"]) - entry_price) / entry_price) * 100
            entry_price = row["close"]
            continue

        if in_position:
            pnl_pct = ((row["close"] - entry_price) / entry_price) * 100
            exit_signal = (
                row["rsi"] > strategy.rsi_sell_threshold
                or pnl_pct <= -strategy.stop_loss_pct
                or pnl_pct >= strategy.take_profit_pct
            )
            if exit_signal:
                pnl = balance * (pnl_pct / 100)
                balance += pnl
                equity_curve.append(balance)
                if pnl >= 0:
                    wins += 1
                    gross_profit += pnl
                else:
                    losses += 1
                    gross_loss += abs(pnl)
                in_position = False

    if in_position:
        final_price = float(df.iloc[-1]["close"])
        final_price = df.iloc[-1]["close"]
        pnl_pct = ((final_price - entry_price) / entry_price) * 100
        pnl = balance * (pnl_pct / 100)
        balance += pnl
        equity_curve.append(balance)
        if pnl >= 0:
            wins += 1
            gross_profit += pnl
        else:
            losses += 1
            gross_loss += abs(pnl)

    total_trades = wins + losses
    total_return = ((balance - request.initial_balance) / request.initial_balance) * 100
    win_rate = (wins / total_trades) * 100 if total_trades else 0.0
    profit_factor = (gross_profit / gross_loss) if gross_loss else float("inf") if gross_profit else 0.0

    equity_series = pd.Series(equity_curve)
    rolling_peak = equity_series.cummax()
    drawdown = ((equity_series - rolling_peak) / rolling_peak) * 100
    max_drawdown = abs(float(drawdown.min())) if not drawdown.empty else 0.0
    max_drawdown = abs(drawdown.min()) if not drawdown.empty else 0.0

    returns = equity_series.pct_change().dropna()
    sharpe = (
        float(math.sqrt(252) * returns.mean() / returns.std())
        if len(returns) > 1 and returns.std() != 0
        else 0.0
    )

    metrics = BacktestMetrics(
        total_return_pct=round(total_return, 2),
        win_rate_pct=round(win_rate, 2),
        profit_factor=round(profit_factor, 4) if math.isfinite(profit_factor) else profit_factor,
        max_drawdown_pct=round(max_drawdown, 2),
        sharpe_ratio=round(sharpe, 4),
        trades=total_trades,
    )
    rounded_curve = [round(x, 2) for x in equity_curve]
    image_path = write_equity_curve_image(rounded_curve)
    return BacktestResponse(metrics=metrics, equity_curve=rounded_curve, chart_image_path=image_path)
    return BacktestResponse(metrics=metrics, equity_curve=[round(x, 2) for x in equity_curve])


def strategy_with_params(base: StrategyDefinition, rsi_buy: int, rsi_sell: int, ema: int) -> StrategyDefinition:
    return StrategyDefinition(
        pair=base.pair,
        timeframe=base.timeframe,
        entry_rule=base.entry_rule,
        exit_rule=base.exit_rule,
        stop_loss_pct=base.stop_loss_pct,
        take_profit_pct=base.take_profit_pct,
        rsi_period=base.rsi_period,
        rsi_buy_threshold=rsi_buy,
        rsi_sell_threshold=rsi_sell,
        ema_period=ema,
    )
