# ForexMind AI — Strategy Builder & Backtesting Platform

Production-minded backend MVP for an AI-powered Forex strategy research platform.

## What is implemented

- **Automatic strategy generation** by pair/timeframe/risk profile.
- **Automatic data generation** (`/data/fetch`) to bootstrap testing without external APIs.
- **Backtesting engine** with risk metrics:
This repository now contains a working backend MVP for an AI-powered Forex strategy research platform.

## What is implemented

- **Strategy Generator API**: Produces a parameterized strategy from pair, timeframe, and risk tolerance.
- **Backtesting Engine API**: Simulates trades on OHLC candles and computes:
  - Total return %
  - Win rate %
  - Profit factor
  - Max drawdown %
  - Sharpe ratio
- **Automatic chart image generation** for equity curve (`.png`) after each backtest.
- **Parameter optimization** (`/optimize`) over RSI/EMA combinations.
- **One-shot pipeline** (`/pipeline/run`) that fetches data, generates strategy, backtests, and optimizes in a single request.

## API routes

- `GET /health`
- `POST /strategy/generate`
- `POST /data/fetch`
- `POST /backtest`
- `POST /optimize`
- `POST /pipeline/run`
- `GET /artifacts/<image>.png` for generated equity charts

## Quick start (local)
  - Equity curve
- **Strategy Optimizer API**: Runs a grid search across RSI and EMA combinations and returns the best strategy/metrics.

## Project structure

```text
backend/
  app/
    main.py               # FastAPI app + routes
    models.py             # API contracts
    strategy_generator.py # Rule-based strategy generation
    backtester.py         # Core backtest logic + metrics
    optimizer.py          # Parameter optimization loop
  requirements.txt
```

## Quick start

1. Create virtual environment and install dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open docs: http://127.0.0.1:8000/docs

## Easy deployment

### Docker Compose (recommended)

```bash
docker compose up --build
```

API: http://localhost:8000

### Docker only

```bash
docker build -t forexmind-api ./backend
docker run -p 8000:8000 forexmind-api
```

## Example: fully automatic workflow

Call `/pipeline/run` with:

```json
{
  "pair": "EUR/USD",
  "timeframe": "1H",
  "risk_tolerance": "medium",
  "points": 300,
  "initial_balance": 10000
}
```

Response includes strategy, backtest metrics, optimization output, and chart image path.

## Notes

- Current data source is a robust synthetic data generator to keep startup simple and deterministic.
- You can later swap in Alpha Vantage/Twelve Data/Oanda behind `data_provider.py` without changing public API contracts.
```

2. Run the API:

```bash
uvicorn app.main:app --reload
```

3. Open docs:

- http://127.0.0.1:8000/docs

## Example workflow

1. Call `/strategy/generate` with:
   - `pair = "EUR/USD"`
   - `timeframe = "1H"`
   - `risk_tolerance = "medium"`
2. Use response strategy in `/backtest` with historical candles.
3. Use `/optimize` to find stronger RSI/EMA parameters over the same candle set.

## Notes

- The current generator is deterministic/rule-based for a reliable MVP. You can later plug in OpenAI API responses behind the same contract.
- The optimizer currently uses grid search; this can evolve into genetic optimization in a future iteration.
