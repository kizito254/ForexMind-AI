from __future__ import annotations

from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def write_equity_curve_image(equity_curve: list[float], output_dir: str = "backend/artifacts") -> str | None:
    if len(equity_curve) < 2:
        return None

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    filename = f"equity_curve_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.png"
    full_path = out_path / filename

    plt.figure(figsize=(9, 4.5))
    plt.plot(equity_curve, color="#2563eb", linewidth=2)
    plt.title("Backtest Equity Curve")
    plt.xlabel("Trade #")
    plt.ylabel("Balance")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(full_path, dpi=140)
    plt.close()
    return str(full_path)
