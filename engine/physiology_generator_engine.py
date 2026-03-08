import csv
import json
import numpy as np
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

INPUT_FILE = DATA_PATH / "btc_monthly_ohlcv.csv"
OUTPUT_DIR = DATA_PATH / "organism_metrics"


def load_data():

    rows = []

    with open(INPUT_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:

            rows.append(r)

    return rows


def compute_metrics(rows):

    closes = [float(r["close"]) for r in rows]

    returns = np.diff(closes) / closes[:-1]

    volatility = np.std(returns)

    heartbeat_variability = np.std(returns)

    arrhythmia_index = np.mean(np.abs(returns))

    structural_tension = np.max(np.abs(returns))

    volatility_resonance = volatility

    return {
        "heartbeat_variability": float(heartbeat_variability),
        "arrhythmia_index": float(arrhythmia_index),
        "structural_tension": float(structural_tension),
        "volatility_resonance": float(volatility_resonance)
    }


def save_metrics(rows, metrics):

    for r in rows:

        date = r["date"]

        year, month = date.split("-")

        name = f"bitcoin_{year}_{month}_metrics.json"

        path = OUTPUT_DIR / name

        with open(path, "w") as f:

            json.dump(metrics, f, indent=4)


def main():

    print("\nBitcoin Organism — Physiology Generator")
    print("--------------------------------------------------")

    rows = load_data()

    metrics = compute_metrics(rows)

    save_metrics(rows, metrics)

    print("Physiological metrics generated")

    print("Output directory:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
