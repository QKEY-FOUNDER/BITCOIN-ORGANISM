import json
import math
import os
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"


def load_metrics():

    records = []

    for f in os.listdir(METRICS_PATH):

        if not f.endswith("_metrics.json"):
            continue

        if "FULL" in f:
            continue

        with open(METRICS_PATH / f) as j:
            metrics = json.load(j)

        if metrics["structural_tension"] is None:
            continue

        month = f.replace("_metrics.json", "")

        vector = [
            metrics["heartbeat_variability"],
            metrics["arrhythmia_index"],
            metrics["structural_tension"],
            metrics["volatility_resonance"]
        ]

        records.append((month, vector))

    records.sort()

    return records


def distance(a, b):

    return math.sqrt(sum((x-y)**2 for x, y in zip(a,b)))


def find_similar_states(records):

    current_month, current_vector = records[-1]

    similarities = []

    for month, vector in records[:-1]:

        d = distance(current_vector, vector)

        similarities.append((month, d))

    similarities.sort(key=lambda x: x[1])

    return current_month, similarities[:10]


def main():

    print("\nBitcoin Organism - Evolution Time Machine")
    print("--------------------------------------------------")

    records = load_metrics()

    current_month, similar = find_similar_states(records)

    print("Current organism state:", current_month)

    print("\nMost similar historical states:\n")

    for month, d in similar:

        print(month, "→ distance:", round(d,4))


if __name__ == "__main__":
    main()
