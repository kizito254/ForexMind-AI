from __future__ import annotations

from .models import StrategyDefinition, StrategyRequest


RISK_PROFILES = {
    "low": {"stop_loss_pct": 0.5, "take_profit_pct": 1.0, "rsi_buy": 25, "rsi_sell": 75, "ema": 100},
    "medium": {"stop_loss_pct": 1.0, "take_profit_pct": 2.0, "rsi_buy": 30, "rsi_sell": 70, "ema": 50},
    "high": {"stop_loss_pct": 1.5, "take_profit_pct": 3.0, "rsi_buy": 35, "rsi_sell": 65, "ema": 21},
}


def generate_strategy(payload: StrategyRequest) -> StrategyDefinition:
    config = RISK_PROFILES[payload.risk_tolerance]
    entry = (
        f"Buy {payload.pair} when RSI({14}) < {config['rsi_buy']} "
        f"and close price crosses above EMA({config['ema']})."
    )
    exit_rule = (
        f"Sell when RSI({14}) > {config['rsi_sell']} or stop-loss/take-profit is hit."
    )

    return StrategyDefinition(
        pair=payload.pair,
        timeframe=payload.timeframe,
        entry_rule=entry,
        exit_rule=exit_rule,
        stop_loss_pct=config["stop_loss_pct"],
        take_profit_pct=config["take_profit_pct"],
        rsi_period=14,
        rsi_buy_threshold=config["rsi_buy"],
        rsi_sell_threshold=config["rsi_sell"],
        ema_period=config["ema"],
    )
