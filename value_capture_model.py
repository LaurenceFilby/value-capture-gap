"""
Value Capture Gap: career band model.

Generates the value / pay / market-alternative trajectories used by the
interactive page (index.html) and exports them to CSV. Mirrors the JavaScript
model in index.html so results can be reproduced and extended in Python.

Usage:
    python model/value_capture_model.py            # writes data/band_model.csv
    python model/value_capture_model.py --plot     # also shows a matplotlib chart

Author: Laurence Filby
"""
import argparse
import csv
import math
from pathlib import Path

# Pay anchors: SSA 2022 wage percentiles (mid-career pay for each tier).
# Ceiling/floor ratios: mid-career ratios from the original v1 model.
TIERS = {
    "Median":    {"anchor": 40_831,    "value_ratio": 1.667, "alt_ratio": 0.667},
    "Top 10%":   {"anchor": 122_502,   "value_ratio": 1.80,  "alt_ratio": 0.70},
    "Top 1%":    {"anchor": 375_716,   "value_ratio": 1.70,  "alt_ratio": 0.57},
    "Top 0.1%":  {"anchor": 1_219_539, "value_ratio": 1.79,  "alt_ratio": 0.54},
    "Top 0.01%": {"anchor": 4_859_651, "value_ratio": 2.55,  "alt_ratio": 0.70},
}

S20 = 0.48 + 0.52 * (1 - math.exp(-20 / 9))


def career_shape(t: float) -> float:
    """Pay relative to the year-20 anchor: fast early growth, plateau, gentle late decline."""
    base = (0.48 + 0.52 * (1 - math.exp(-t / 9))) / S20
    return base - (0.012 * (t - 32) if t > 32 else 0.0)


def band(tier: str, strategy: str | None = None, capture_adj: float = 0.0, step: float = 0.5):
    """Return rows of (year, value_created, pay, market_alternative).

    strategy: None | "floor" | "ceiling" | "capture"
    capture_adj: -0.30..0.60, moves pay toward the ceiling (positive) or the floor (negative).
    """
    cfg = TIERS[tier]
    rows = []
    t = 0.0
    while t <= 40 + 1e-9:
        base = cfg["anchor"] * career_shape(t)
        prog = t / 20
        value = base * (1 + (cfg["value_ratio"] - 1) * min(1.25, 0.55 + 0.45 * prog))
        alt = base * (1 - (1 - cfg["alt_ratio"]) * min(1.2, 0.6 + 0.4 * prog))
        pay = base
        if strategy == "floor":        # Strategy I: raise the reservation wage
            lift = alt * 0.25
            alt += lift
            pay += lift * 0.7
        elif strategy == "ceiling":    # Strategy II: create more value
            value *= 1.3
        elif strategy == "capture":    # Strategy III: capture more of the surplus
            pay += (value - pay) * 0.3
        pay += (value - pay) * capture_adj if capture_adj >= 0 else (pay - alt) * capture_adj
        pay = min(max(pay, alt * 1.001), value * 0.999)
        rows.append((t, value, pay, alt))
        t += step
    return rows


def capture_share(value: float, pay: float, alt: float) -> float:
    """Share of the surplus (value - alternative) that the worker captures."""
    return (pay - alt) / (value - alt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    out = Path(__file__).resolve().parent.parent / "data" / "band_model.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tier", "strategy", "year", "value_created", "pay", "market_alternative", "capture_share"])
        for tier in TIERS:
            for strat in (None, "floor", "ceiling", "capture"):
                for t, v, p, a in band(tier, strat):
                    w.writerow([tier, strat or "baseline", t, round(v), round(p), round(a), round(capture_share(v, p, a), 4)])
    print(f"Wrote {out}")

    if args.plot:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(11, 6))
        for tier in TIERS:
            rows = band(tier)
            ys = list(zip(*rows))
            ax.fill_between(ys[0], ys[2], ys[1], alpha=0.15)
            ax.plot(ys[0], ys[2], lw=2.5, label=tier)
        ax.set_yscale("log")
        ax.set_xlabel("Career year")
        ax.set_ylabel("Annual $")
        ax.set_title("Value Capture Gap: pay (line) and uncaptured value (shaded)")
        ax.legend()
        plt.show()


if __name__ == "__main__":
    main()
