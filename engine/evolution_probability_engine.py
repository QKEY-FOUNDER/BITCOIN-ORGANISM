import os
import json
import math
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
PRESSURE_PATH = BASE_PATH / "data" / "evolution_pressure.csv"


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


def load_pressure():

    series = []

    with open(PRESSURE_PATH) as f:

        reader = csv.DictReader(f)

        for row in reader:

            month = row["month"]
            pressure = float(row["pressure"])

            series.append((month, pressure))

    return series


def distance(a, b):

    d = 0

    d += (a["heartbeat_variability"] - b["heartbeat_variability"]) ** 2
    d += (a["arrhythmia_index"] - b["arrhythmia_index"]) ** 2
    d += (a["structural_tension"] - b["structural_tension"]) ** 2
    d += (a["volatility_resonance"] - b["volatility_resonance"]) ** 2

    return math.sqrt(d)


def main():

    print("\nBitcoin Organism — Evolution Probability Engine")
    print("--------------------------------------------------")

    metrics_records = load_metrics()
    pressure_series = load_pressure()

    pressure_dict = dict(pressure_series)

    current_month, current_metrics = metrics_records[-1]

    print("Current state:", current_month)
    print("")

    similarities = []

    for month, metrics in metrics_records[:-1]:

        d = distance(current_metrics, metrics)

        similarities.append((month, d))

    similarities.sort(key=lambda x: x[1])

    analogs = similarities[:10]

    print("Top analogous states:")
    for m, d in analogs:
        print(m, "distance:", round(d, 4))

    print("")

    months = [m for m, p in pressure_series]

    deltas_3 = []
    deltas_6 = []
    deltas_12 = []

    for month, d in analogs:

        if month not in pressure_dict:
            continue

        index = months.index(month)

        base_pressure = pressure_dict[month]

        if index + 3 < len(months):

            future_month = months[index + 3]
            future_pressure = pressure_dict[future_month]

            deltas_3.append(future_pressure - base_pressure)

        if index + 6 < len(months):

            future_month = months[index + 6]
            future_pressure = pressure_dict[future_month]

            deltas_6.append(future_pressure - base_pressure)

        if index + 12 < len(months):

            future_month = months[index + 12]
            future_pressure = pressure_dict[future_month]

            deltas_12.append(future_pressure - base_pressure)

    def avg(x):

        if len(x) == 0:
            return 0

        return sum(x) / len(x)

    print("\nAverage pressure evolution after analogous states:\n")

    print("+3 months :", round(avg(deltas_3), 3))
    print("+6 months :", round(avg(deltas_6), 3))
    print("+12 months:", round(avg(deltas_12), 3))

    print("\nSample sizes:")
    print("3 months :", len(deltas_3))
    print("6 months :", len(deltas_6))
    print("12 months:", len(deltas_12))


if __name__ == "__main__":
    main()
