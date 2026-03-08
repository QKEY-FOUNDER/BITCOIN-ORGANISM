import os
import json
import statistics
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


def compute_trend(values):

    if len(values) < 2:
        return 0

    return values[-1] - values[0]


def normalize(x, scale):

    if scale == 0:
        return 0

    return x / scale


def main():

    print("\nBitcoin Organism — Critical Transition Detector")
    print("--------------------------------------------------")

    records = load_metrics()

    window = records[-12:]

    hbv = [m["heartbeat_variability"] for _, m in window]
    arr = [m["arrhythmia_index"] for _, m in window]
    tension = [m["structural_tension"] for _, m in window]
    vol = [m["volatility_resonance"] for _, m in window]

    trend_hbv = compute_trend(hbv)
    trend_arr = compute_trend(arr)
    trend_tension = compute_trend(tension)
    trend_vol = compute_trend(vol)

    score = (
        normalize(trend_hbv, 0.05) +
        normalize(trend_arr, 0.1) +
        normalize(trend_tension, 0.5) +
        normalize(trend_vol, 1.0)
    ) / 4

    probability = max(0, min(score, 1))

    print("Trend signals (last 12 months):\n")

    print("heartbeat_variability trend:", round(trend_hbv, 4))
    print("arrhythmia_index trend:", round(trend_arr, 4))
    print("structural_tension trend:", round(trend_tension, 4))
    print("volatility_resonance trend:", round(trend_vol, 4))

    print("\nCritical Transition Probability:")

    print(round(probability, 3))

    if probability > 0.7:

        print("\nSignal: HIGH probability of regime transition")

    elif probability > 0.4:

        print("\nSignal: EARLY structural instability")

    else:

        print("\nSignal: System relatively stable")


if __name__ == "__main__":
    main()
