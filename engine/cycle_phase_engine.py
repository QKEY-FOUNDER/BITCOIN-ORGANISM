import os
import json
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"
METRICS_PATH = DATA_PATH / "organism_metrics"
PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"


def load_latest_metrics():

    records = []

    for f in os.listdir(METRICS_PATH):

        if not f.startswith("bitcoin_"):
            continue

        if not f.endswith("_metrics.json"):
            continue

        if "FULL" in f:
            continue

        with open(METRICS_PATH / f) as j:
            metrics = json.load(j)

        if metrics["structural_tension"] is None:
            continue

        month = f.replace("_metrics.json", "")

        records.append((month, metrics))

    records.sort()

    return records[-1]


def load_pressure_series():

    series = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            series.append(
                (row["month"], float(row["pressure"]))
            )

    return series


def compute_pressure_trend(series, window=6):

    pressures = [p for _, p in series[-window:]]

    return pressures[-1] - pressures[0]


def detect_phase(pressure, trend, tension, volatility):

    if pressure < 1.8 and tension < 0.3:
        return "Accumulation"

    if pressure < 3.0 and trend > 0:
        return "Expansion"

    if pressure >= 3.0 and tension > 0.4:
        return "Distribution"

    if trend < 0:
        return "Compression"

    return "Transition"


def main():

    print("\nBitcoin Organism — Cycle Phase Detector")
    print("--------------------------------------------------")

    month, metrics = load_latest_metrics()

    series = load_pressure_series()

    _, pressure = series[-1]

    trend = compute_pressure_trend(series)

    tension = metrics["structural_tension"]
    volatility = abs(metrics["volatility_resonance"])

    phase = detect_phase(
        pressure,
        trend,
        tension,
        volatility
    )

    print("Current state:", month)
    print("")
    print("Pressure:", round(pressure,3))
    print("Pressure trend:", round(trend,3))
    print("Structural tension:", round(tension,3))
    print("Volatility:", round(volatility,3))
    print("")
    print("Detected Cycle Phase:")
    print(phase)


if __name__ == "__main__":
    main()
