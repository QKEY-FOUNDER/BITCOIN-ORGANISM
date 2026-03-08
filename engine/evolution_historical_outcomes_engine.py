import json
import math
import os
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"


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


def load_pressure():

    data = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:

            month = r["month"]
            pressure = float(r["pressure"])

            data.append((month, pressure))

    return data


def distance(a,b):

    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))


def find_similar(records):

    current_month, current_vector = records[-1]

    similarities = []

    for month, vector in records[:-1]:

        d = distance(current_vector, vector)

        similarities.append((month, d))

    similarities.sort(key=lambda x: x[1])

    return current_month, similarities[:5]


def pressure_after(month, pressure_series, months_ahead):

    for i,(m,p) in enumerate(pressure_series):

        if m == month:

            future_index = i + months_ahead

            if future_index < len(pressure_series):

                return pressure_series[future_index][1]

    return None


def main():

    print("\nBitcoin Organism - Historical Outcome Analysis")
    print("--------------------------------------------------")

    records = load_metrics()

    pressure_series = load_pressure()

    current_month, similar = find_similar(records)

    print("Current organism state:", current_month)

    print("\nHistorical analogues and outcomes:\n")

    for month,d in similar:

        p3 = pressure_after(month, pressure_series, 3)
        p6 = pressure_after(month, pressure_series, 6)
        p12 = pressure_after(month, pressure_series, 12)

        print(month,"distance:",round(d,4))

        print("  +3 months :", p3)
        print("  +6 months :", p6)
        print("  +12 months:", p12)

        print("")


if __name__ == "__main__":
    main()
