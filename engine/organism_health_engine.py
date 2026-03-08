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


def load_pressure():

    series = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            series.append((row["month"], float(row["pressure"])))

    return series[-1]


def normalize(v, min_v, max_v):

    if max_v == min_v:
        return 0

    x = (v - min_v) / (max_v - min_v)

    return max(0, min(x, 1))


def compute_health_index(pressure, resilience, transition_risk):

    pressure_score = normalize(pressure, 0, 4)
    resilience_score = resilience
    stability_score = 1 - transition_risk

    health = (
        pressure_score * 0.35 +
        resilience_score * 0.40 +
        stability_score * 0.25
    )

    return round(health * 100, 2)


def classify_health(score):

    if score > 80:
        return "Strong Expansion"

    if score > 60:
        return "Healthy Expansion"

    if score > 40:
        return "Neutral / Compression"

    if score > 25:
        return "Structural Stress"

    return "Critical Instability"


def main():

    print("\nBitcoin Organism — Health Index")
    print("--------------------------------------------------")

    month, metrics = load_latest_metrics()

    _, pressure = load_pressure()

    tension = metrics["structural_tension"]
    vol = abs(metrics["volatility_resonance"])

    resilience = 1 - min(1, (tension + vol) / 2)

    transition_risk = min(1, tension * 0.8 + vol * 0.2)

    health_index = compute_health_index(
        pressure,
        resilience,
        transition_risk
    )

    status = classify_health(health_index)

    print("Current state:", month)
    print("")
    print("Pressure:", round(pressure,3))
    print("Resilience:", round(resilience,3))
    print("Transition risk:", round(transition_risk,3))
    print("")
    print("Health Index:", health_index)
    print("Status:", status)


if __name__ == "__main__":
    main()
