from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .backtester import run_backtest
from .data_provider import fetch_candles
from .models import (
    BacktestRequest,
    BacktestResponse,
    DataFetchRequest,
    DataFetchResponse,
    OptimizationRequest,
    OptimizationResponse,
    PipelineRequest,
    PipelineResponse,

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

app = FastAPI(title="AI Forex Strategy Builder", version="0.2.0")
app.mount("/artifacts", StaticFiles(directory="backend/artifacts"), name="artifacts")
app = FastAPI(title="AI Forex Strategy Builder", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/strategy/generate", response_model=StrategyDefinition)
def create_strategy(payload: StrategyRequest) -> StrategyDefinition:
    return generate_strategy(payload)


@app.post("/data/fetch", response_model=DataFetchResponse)
def data_fetch(payload: DataFetchRequest) -> DataFetchResponse:
    return fetch_candles(payload)


@app.post("/backtest", response_model=BacktestResponse)
def backtest(payload: BacktestRequest) -> BacktestResponse:
    return run_backtest(payload)


@app.post("/optimize", response_model=OptimizationResponse)
def optimize(payload: OptimizationRequest) -> OptimizationResponse:
    return optimize_strategy(payload)


@app.post("/pipeline/run", response_model=PipelineResponse)
def run_full_pipeline(payload: PipelineRequest) -> PipelineResponse:
    strategy = generate_strategy(
        StrategyRequest(
            pair=payload.pair,
            timeframe=payload.timeframe,
            risk_tolerance=payload.risk_tolerance,
        )
    )
    fetched = fetch_candles(
        DataFetchRequest(pair=payload.pair, timeframe=payload.timeframe, points=payload.points)
    )
    backtest_result = run_backtest(
        BacktestRequest(strategy=strategy, candles=fetched.candles, initial_balance=payload.initial_balance)
    )
    optimization = optimize_strategy(
        OptimizationRequest(
            pair=payload.pair,
            timeframe=payload.timeframe,
            candles=fetched.candles,
            initial_balance=payload.initial_balance,
        )
    )
    return PipelineResponse(
        strategy=strategy,
        backtest=backtest_result,
        optimizer=optimization,
        data_source=fetched.source,
    )
