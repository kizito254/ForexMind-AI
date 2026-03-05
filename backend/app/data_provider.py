from __future__ import annotations

from datetime import datetime, timedelta
import math
import random

from .models import Candle, DataFetchRequest, DataFetchResponse


def _parse_timeframe_to_minutes(timeframe: str) -> int:
    tf = timeframe.strip().upper()
    if tf.endswith("M") and tf[:-1].isdigit():
        return int(tf[:-1])
    if tf.endswith("H") and tf[:-1].isdigit():
        return int(tf[:-1]) * 60
    if tf.endswith("D") and tf[:-1].isdigit():
        return int(tf[:-1]) * 60 * 24
    raise ValueError("Unsupported timeframe. Use formats like 15M, 1H, 4H, 1D.")


def _synthetic_candles(points: int, timeframe_minutes: int) -> list[Candle]:
    candles: list[Candle] = []
    now = datetime.utcnow()
    base = 1.10

    for idx in range(points):
        t = now - timedelta(minutes=(points - idx) * timeframe_minutes)
        cycle = math.sin(idx / 16) * 0.0025
        trend = idx * 0.000015
        noise = random.uniform(-0.0004, 0.0004)
        close = max(0.01, base + cycle + trend + noise)
        open_price = close + random.uniform(-0.0003, 0.0003)
        high = max(open_price, close) + random.uniform(0.0001, 0.0005)
        low = min(open_price, close) - random.uniform(0.0001, 0.0005)
        candles.append(Candle(timestamp=t, open=open_price, high=high, low=low, close=close))

    return candles


def fetch_candles(payload: DataFetchRequest) -> DataFetchResponse:
    timeframe_minutes = _parse_timeframe_to_minutes(payload.timeframe)
    candles = _synthetic_candles(points=payload.points, timeframe_minutes=timeframe_minutes)
    return DataFetchResponse(candles=candles, source="synthetic-generator")
