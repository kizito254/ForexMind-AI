from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Candle(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float


class StrategyRequest(BaseModel):
    pair: str = Field(..., examples=["EUR/USD"])
    timeframe: str = Field(..., examples=["1H"])
    risk_tolerance: Literal["low", "medium", "high"] = "medium"


class StrategyDefinition(BaseModel):
    pair: str
    timeframe: str
    entry_rule: str
    exit_rule: str
    stop_loss_pct: float
    take_profit_pct: float
    rsi_period: int
    rsi_buy_threshold: int
    rsi_sell_threshold: int
    ema_period: int


class BacktestRequest(BaseModel):
    strategy: StrategyDefinition
    candles: list[Candle]
    initial_balance: float = 10_000


class BacktestMetrics(BaseModel):
    total_return_pct: float
    win_rate_pct: float
    profit_factor: float
    max_drawdown_pct: float
    sharpe_ratio: float
    trades: int


class BacktestResponse(BaseModel):
    metrics: BacktestMetrics
    equity_curve: list[float]
    chart_image_path: str | None = None


class OptimizationRequest(BaseModel):
    pair: str
    timeframe: str
    candles: list[Candle]
    initial_balance: float = 10_000
    rsi_buy_values: list[int] = [20, 25, 30]
    rsi_sell_values: list[int] = [70, 75, 80]
    ema_values: list[int] = [50, 100]


class OptimizationResponse(BaseModel):
    best_strategy: StrategyDefinition
    best_metrics: BacktestMetrics
    tried_combinations: int


class DataFetchRequest(BaseModel):
    pair: str = Field(..., examples=["EUR/USD"])
    timeframe: str = Field("1H", examples=["1H", "4H"])
    points: int = Field(300, ge=100, le=5000)


class DataFetchResponse(BaseModel):
    candles: list[Candle]
    source: str


class PipelineRequest(BaseModel):
    pair: str = Field(..., examples=["EUR/USD"])
    timeframe: str = Field("1H")
    risk_tolerance: Literal["low", "medium", "high"] = "medium"
    points: int = Field(300, ge=100, le=5000)
    initial_balance: float = 10_000


class PipelineResponse(BaseModel):
    strategy: StrategyDefinition
    backtest: BacktestResponse
    optimizer: OptimizationResponse
    data_source: str
