import os
from pathlib import Path

from engine.phase_memory import HISTORY_PATH
from engine.phase_memory import update_phase_history, compute_regime_duration
from engine.metrics_engine import compute_market_biometrics
from engine.phase_engine import classify_market_phase


BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

TARGET_MONTHS = [
    "bitcoin_2020_02.csv",
    "bitcoin_2020_03.csv",
    "bitcoin_2020_04.csv",

    "bitcoin_2021_10.csv",
    "bitcoin_2021_11.csv",
    "bitcoin_2021_12.csv",

    "bitcoin_2022_05.csv",
    "bitcoin_2022_06.csv",
    "bitcoin_2022_07.csv",
]


def find_csv(month_name):
    for root, _, files in os.walk(DATA_PATH):
        if month_name in files:
            return Path(root) / month_name
    return None


def compute_delta(current, previous):
    delta = {}
    for k in current:
        if isinstance(current[k], (int, float)):
            delta[k] = current[k] - previous.get(k, 0)
    return delta


def compute_acceleration(delta, previous_delta):
    acc = {}

    acc["volatility_acceleration"] = (
        delta.get("volatility_resonance", 0)
        - previous_delta.get("volatility_resonance", 0)
    )

    acc["geo_entropy_delta"] = delta.get("geo_entropy", 0)

    acc["arrhythmia_slope"] = (
        delta.get("arrhythmia_index", 0)
        - previous_delta.get("arrhythmia_index", 0)
    )

    return acc


def main():

    print("Phase Backtest — Multi-Cycle Validation with Memory")
    print("--------------------------------------------------")

        # --------------------------------------------------
    # Reset histórico para backtest limpo
    # --------------------------------------------------

    if HISTORY_PATH.exists():
        HISTORY_PATH.unlink()

    previous_metrics = None
    previous_delta = None
    previous_phase = None
    previous_count = 0

    for month in TARGET_MONTHS:

        csv_path = find_csv(month)

        if not csv_path:
            print(month, "não encontrado.")
            continue

        metrics = compute_market_biometrics(str(csv_path))

        if previous_metrics is None:
            delta = {k: 0.0 for k in metrics}
            acceleration = {
                "volatility_acceleration": 0.0,
                "geo_entropy_delta": 0.0,
                "arrhythmia_slope": 0.0
            }
        else:
            delta = compute_delta(metrics, previous_metrics)
            acceleration = compute_acceleration(delta, previous_delta)

        bundle = {
            "values": metrics,
            "delta": delta,
            "acceleration": acceleration
        }

        phase, count = classify_market_phase(
            bundle,
            previous_phase,
            previous_count
        )

        history = update_phase_history(
            month.replace(".csv", ""),
            phase,
            metrics,
            acceleration
        )

        regime_duration = compute_regime_duration(history)

        print(f"\nMês: {month.replace('.csv','')}")
        print("  structural_tension:", round(metrics["structural_tension"], 6))
        print("  volatility_resonance:", round(metrics["volatility_resonance"], 6))
        print("  volatility_acceleration:", round(acceleration["volatility_acceleration"], 6))
        print("  → Phase:", phase)
        print("  regime_duration:", regime_duration)

        previous_phase = phase
        previous_count = count
        previous_metrics = metrics
        previous_delta = delta


if __name__ == "__main__":
    main()
