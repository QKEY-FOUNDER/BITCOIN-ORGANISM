import os
import json
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
OUTPUT_PATH = BASE_PATH / "data" / "evolution_pressure.csv"


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

        if (
            metrics["structural_tension"] == 0 and
            metrics["heartbeat_variability"] == 0 and
            metrics["arrhythmia_index"] == 0
        ):
            continue

        month = f.replace("_metrics.json", "")

        records.append((month, metrics))

    records.sort()

    return records


def build_pressure_series():

    data = load_metrics()

    series = []

    for month, metrics in data:

        pressure = compute_transition_pressure(metrics)

        series.append({
            "month": month,
            "pressure": pressure,
            "tension": metrics["structural_tension"],
            "volatility": metrics["volatility_resonance"],
            "hbv": metrics["heartbeat_variability"],
            "arrhythmia": metrics["arrhythmia_index"]
        })

    return series


def export_csv(series):

    with open(OUTPUT_PATH, "w", newline="") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "month",
                "pressure",
                "tension",
                "volatility",
                "hbv",
                "arrhythmia"
            ]
        )

        writer.writeheader()

        for row in series:
            writer.writerow(row)


def main():

    print("\nBitcoin Organism — Evolution Pressure Engine")
    print("--------------------------------------------------")

    series = build_pressure_series()

    export_csv(series)

    print("Months processed:", len(series))
    print("Output file:", OUTPUT_PATH)
    print("Evolution pressure timeline created.")


if __name__ == "__main__":
    main()
