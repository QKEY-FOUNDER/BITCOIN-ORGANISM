import csv
import json
import numpy as np
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

INPUT_FILE = DATA_PATH / "btc_monthly_ohlcv.csv"
OUTPUT_DIR = DATA_PATH / "organism_metrics"

WINDOW = 12


def load_data():

    rows = []

    with open(INPUT_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:
            rows.append(r)

    return rows


def compute_metrics(closes):

    returns = np.diff(closes) / closes[:-1]

    heartbeat_variability = np.std(returns)

    arrhythmia_index = np.mean(np.abs(returns))

    structural_tension = np.max(np.abs(returns))

    volatility_resonance = np.std(returns)

    return {
        "heartbeat_variability": float(heartbeat_variability),
        "arrhythmia_index": float(arrhythmia_index),
        "structural_tension": float(structural_tension),
        "volatility_resonance": float(volatility_resonance)
    }


def generate_metrics(rows):

    closes = [float(r["close"]) for r in rows]

    for i in range(WINDOW, len(rows)):

        window_closes = closes[i-WINDOW:i]

        metrics = compute_metrics(window_closes)

        date = rows[i]["date"]

        year, month = date.split("-")

        name = f"bitcoin_{year}_{month}_metrics.json"

        path = OUTPUT_DIR / name

        with open(path, "w") as f:
            json.dump(metrics, f, indent=4)


def main():

    print("\nBitcoin Organism — Rolling Physiology Engine")
    print("--------------------------------------------------")

    rows = load_data()

    generate_metrics(rows)

    print("Rolling physiological metrics generated")
    print("Window size:", WINDOW, "months")
    print("Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
