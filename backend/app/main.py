from __future__ import annotations

from fastapi import FastAPI

from .backtester import run_backtest
from .models import (
    BacktestRequest,
    BacktestResponse,
    OptimizationRequest,
    OptimizationResponse,
    StrategyDefinition,
    StrategyRequest,
)
from .optimizer import optimize_strategy
from .strategy_generator import generate_strategy

app = FastAPI(title="AI Forex Strategy Builder", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/strategy/generate", response_model=StrategyDefinition)
def create_strategy(payload: StrategyRequest) -> StrategyDefinition:
    return generate_strategy(payload)


@app.post("/backtest", response_model=BacktestResponse)
def backtest(payload: BacktestRequest) -> BacktestResponse:
    return run_backtest(payload)


@app.post("/optimize", response_model=OptimizationResponse)
def optimize(payload: OptimizationRequest) -> OptimizationResponse:
    return optimize_strategy(payload)
