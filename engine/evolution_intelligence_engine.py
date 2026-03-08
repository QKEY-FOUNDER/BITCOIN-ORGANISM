import csv
import json
import os
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

            series.append((row["month"], float(row["pressure"])))

    return series


def pressure_trend(series, window=6):

    pressures = [p for _, p in series[-window:]]

    return pressures[-1] - pressures[0]


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def compute_risk(tension, volatility):

    risk = tension * 0.7 + volatility * 0.3

    if risk < 0.2:
        return "Low"

    if risk < 0.5:
        return "Moderate"

    return "High"


def detect_cycle_phase(pressure, trend):

    if pressure < 1.8:
        return "Accumulation"

    if pressure < 3.0 and trend > 0:
        return "Expansion"

    if pressure >= 3.0:
        return "Distribution"

    if trend < 0:
        return "Compression"

    return "Transition"


def strategic_posture(regime, phase, risk):

    if phase == "Accumulation":
        return "Strategic Accumulation Phase"

    if phase == "Expansion" and risk == "Low":
        return "Healthy Bullish Expansion"

    if phase == "Expansion" and risk == "Moderate":
        return "Mature Bullish Expansion"

    if phase == "Distribution":
        return "Late Cycle Distribution"

    if phase == "Compression":
        return "Market Compression / Reset"

    return "Transitional State"


def main():

    print("\nBitcoin Organism — Evolution Intelligence")
    print("--------------------------------------------------")

    month, metrics = load_latest_metrics()

    series = load_pressure_series()

    _, pressure = series[-1]

    trend = pressure_trend(series)

    tension = metrics["structural_tension"]
    volatility = abs(metrics["volatility_resonance"])

    regime = classify_regime(pressure)

    risk = compute_risk(tension, volatility)

    phase = detect_cycle_phase(pressure, trend)

    posture = strategic_posture(regime, phase, risk)

    print("Current state:", month)
    print("")
    print("Pressure:", round(pressure,3))
    print("Trend:", round(trend,3))
    print("Structural tension:", round(tension,3))
    print("Volatility:", round(volatility,3))
    print("")
    print("Regime:", regime)
    print("Cycle phase:", phase)
    print("Risk level:", risk)
    print("")
    print("Strategic Posture:")
    print(posture)


if __name__ == "__main__":
    main()
