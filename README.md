# ForexMind AI — Strategy Builder & Backtesting Platform

This repository now contains a working backend MVP for an AI-powered Forex strategy research platform.

## What is implemented

- **Strategy Generator API**: Produces a parameterized strategy from pair, timeframe, and risk tolerance.
- **Backtesting Engine API**: Simulates trades on OHLC candles and computes:
  - Total return %
  - Win rate %
  - Profit factor
  - Max drawdown %
  - Sharpe ratio
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
