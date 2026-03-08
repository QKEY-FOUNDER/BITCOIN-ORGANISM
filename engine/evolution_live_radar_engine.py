import os
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"


def compute_transition_pressure(metrics):

    hbv = metrics["heartbeat_variability"]
    arr = metrics["arrhythmia_index"]
    tension = metrics["structural_tension"]
    vol = abs(metrics["volatility_resonance"])

    pressure = (
        hbv * 3 +
        arr * 3 +
        tension * 2 +
        vol * 2
    )

    return round(pressure, 6)


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def load_recent_metrics():

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

        if (
            metrics["structural_tension"] == 0 and
            metrics["heartbeat_variability"] == 0 and
            metrics["arrhythmia_index"] == 0
        ):
            continue

        month = f.replace("_metrics.json", "")

        records.append((month, metrics))

    records.sort()

    return records[-5:]


def main():

    print("\nBitcoin Evolution Live Radar")
    print("--------------------------------------------------")

    data = load_recent_metrics()

    for month, metrics in data:

        pressure = compute_transition_pressure(metrics)
        regime = classify_regime(pressure)

        print(month, "-> pressure:", pressure, "| regime:", regime)

    latest_month, latest_metrics = data[-1]

    latest_pressure = compute_transition_pressure(latest_metrics)
    latest_regime = classify_regime(latest_pressure)

    print("\nCurrent Evolution State")
    print("-----------------------")

    print("month:", latest_month)
    print("pressure:", latest_pressure)
    print("regime:", latest_regime)

    print("\nPhysiology Snapshot")

    print("heartbeat_variability:", latest_metrics["heartbeat_variability"])
    print("arrhythmia_index:", latest_metrics["arrhythmia_index"])
    print("structural_tension:", latest_metrics["structural_tension"])
    print("volatility_resonance:", latest_metrics["volatility_resonance"])


if __name__ == "__main__":
    main()
