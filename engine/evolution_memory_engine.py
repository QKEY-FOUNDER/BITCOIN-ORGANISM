import os
import json
import math
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"


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


def distance(a, b):

    d = 0

    d += (a["heartbeat_variability"] - b["heartbeat_variability"]) ** 2
    d += (a["arrhythmia_index"] - b["arrhythmia_index"]) ** 2
    d += (a["structural_tension"] - b["structural_tension"]) ** 2
    d += (a["volatility_resonance"] - b["volatility_resonance"]) ** 2

    return math.sqrt(d)


def main():

    print("\nBitcoin Organism — Evolution Memory")
    print("--------------------------------------------------")

    records = load_metrics()

    current_month, current_metrics = records[-1]

    print("Current state:", current_month)
    print("")

    similarities = []

    for month, metrics in records[:-1]:

        d = distance(current_metrics, metrics)

        similarities.append((month, d))

    similarities.sort(key=lambda x: x[1])

    print("Most similar historical states:\n")

    for month, d in similarities[:10]:

        print(month, "→ distance:", round(d, 4))


if __name__ == "__main__":
    main()
