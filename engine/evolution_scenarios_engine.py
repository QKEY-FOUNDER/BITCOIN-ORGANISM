import os
import json
import csv
import math
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
PRESSURE_CSV = BASE_PATH / "data" / "evolution_pressure.csv"


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


def load_metrics():
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

    return records


def load_pressure_series():
    series = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            series.append(
                (row["month"], float(row["pressure"]))
            )

    return series


def distance(m1, m2):

    d = 0

    d += (m1["structural_tension"] - m2["structural_tension"]) ** 2
    d += (m1["volatility_resonance"] - m2["volatility_resonance"]) ** 2
    d += (m1["heartbeat_variability"] - m2["heartbeat_variability"]) ** 2
    d += (m1["arrhythmia_index"] - m2["arrhythmia_index"]) ** 2

    return math.sqrt(d)


def future_pressure(month, pressure_series, horizon):

    months = [m for m, _ in pressure_series]

    if month not in months:
        return None

    i = months.index(month)

    if i + horizon >= len(pressure_series):
        return None

    return pressure_series[i + horizon][1]


def main():

    print("\nBitcoin Organism — Evolution Scenarios")
    print("--------------------------------------------------")

    metrics = load_metrics()
    pressure_series = load_pressure_series()

    current_month, current_metrics = metrics[-1]

    print("Current state:", current_month)

    distances = []

    for m, data in metrics[:-1]:

        d = distance(current_metrics, data)

        distances.append((m, d))

    distances.sort()

    top = distances[:10]

    print("\nTop analogous states:")

    for m, d in top:
        print(m, "distance:", round(d, 4))

    horizons = [3, 6, 12]

    scenario_results = {h: [] for h in horizons}

    for month, dist in top:

        for h in horizons:

            fp = future_pressure(month, pressure_series, h)

            if fp is None:
                continue

            regime = classify_regime(fp)

            scenario_results[h].append(regime)

    print("\nScenario probabilities:\n")

    for h in horizons:

        outcomes = scenario_results[h]

        if len(outcomes) == 0:
            continue

        counts = {}

        for o in outcomes:
            counts[o] = counts.get(o, 0) + 1

        print(str(h) + " months ahead:")

        total = len(outcomes)

        for regime, c in counts.items():

            p = c / total

            print(regime, "→", round(p, 3))

        print("")


if __name__ == "__main__":
    main()
