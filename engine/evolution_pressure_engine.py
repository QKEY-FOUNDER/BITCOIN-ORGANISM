import os
import json
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

MACRO_FILE = BASE_PATH / "data" / "macro_environment_state.json"

def get_macro_modifier():

    try:

        with open(MACRO_FILE) as f:
            data = json.load(f)

        state = data.get("macro_environment")

        if state == "Macro Expansion":
            return 0.2

        if state == "Financial Stress":
            return -0.2

        return 0

    except:

        return 0

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
OUTPUT_PATH = BASE_PATH / "data" / "evolution_pressure.csv"
LIQUIDITY_FILE = BASE_PATH / "data" / "liquidity_state.json"

def get_liquidity_modifier():
    try:
        with open(LIQUIDITY_FILE) as f:
            data = json.load(f)
        state = data.get("liquidity_regime")
        if state == "Global Liquidity Expansion":
            return 0.35
        if state == "Global Liquidity Contraction":
            return -0.35
        if state == "Liquidity Stress Environment":
            return -0.15
        return 0.0
    except:
        return 0.0

def get_liquidity_modifier():

    liquidity_file = BASE_PATH / "data" / "liquidity_state.json"

    if not liquidity_file.exists():
        return 0

    try:

        with open(liquidity_file) as f:
            data = json.load(f)

        regime = data.get("liquidity_regime")

        if regime == "Global Liquidity Expansion":
            return 0.2

        if regime == "Global Liquidity Contraction":
            return -0.2

        if regime == "Liquidity Stress Environment":
            return -0.1

        return 0

    except:

        return 0

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
    liquidity_modifier = get_liquidity_modifier()
    pressure = pressure + liquidity_modifier
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
