import os
import json
import math
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
PRESSURE_PATH = BASE_PATH / "data" / "evolution_pressure.csv"


def load_pressure():

    series = []

    with open(PRESSURE_PATH) as f:

        reader = csv.DictReader(f)

        for row in reader:

            month = row["month"]
            pressure = float(row["pressure"])

            series.append((month, pressure))

    return series


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

    print("\nBitcoin Organism — Evolution Future Paths")
    print("--------------------------------------------------")

    records = load_metrics()
    pressure = load_pressure()

    pressure_dict = dict(pressure)

    current_month, current_metrics = records[-1]

    print("Current state:", current_month)
    print("")

    similarities = []

    for month, metrics in records[:-1]:

        d = distance(current_metrics, metrics)

        similarities.append((month, d))

    similarities.sort(key=lambda x: x[1])

    top_states = similarities[:5]

    print("Analysing future paths of similar states:\n")

    for month, d in top_states:

        print(month, "(distance:", round(d,4), ")")

        index = [m for m,p in pressure].index(month)

        future_index = index + 12

        if future_index < len(pressure):

            future_month, future_pressure = pressure[future_index]

            current_pressure = pressure_dict[month]

            change = future_pressure - current_pressure

            print(" 12 months later:", future_month)
            print(" pressure change:", round(change,3))
            print("")

        else:

            print(" not enough future data\n")


if __name__ == "__main__":
    main()
