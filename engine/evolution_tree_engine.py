import os
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"


def load_metrics():

    files = []

    for f in os.listdir(METRICS_PATH):
        if f.startswith("bitcoin_") and f.endswith("_metrics.json"):
            files.append(f)

    files.sort()

    dataset = []

    for f in files:

        with open(METRICS_PATH / f) as j:
            metrics = json.load(j)

        month = f.replace("_metrics.json","")

        dataset.append((month, metrics))

    return dataset


def classify_simple(metrics):

    tension = metrics["structural_tension"]

    if tension < 0.25:
        return "Equilibrium"

    if tension < 0.45:
        return "Transition"

    if tension < 0.65:
        return "Expansion"

    return "Instability"


def build_tree():

    data = load_metrics()

    eras = []

    current_phase = None
    start_month = None
    previous_month = None
    phase_count = 0

    MIN_PHASE_DURATION = 4

    for month, metrics in data:

        phase = classify_simple(metrics)

        if current_phase is None:
            current_phase = phase
            start_month = month
            previous_month = month
            phase_count = 1
            continue

        if phase == current_phase:

            phase_count += 1
            previous_month = month
            continue

        if phase_count >= MIN_PHASE_DURATION:

            eras.append({
                "phase": current_phase,
                "start": start_month,
                "end": previous_month
            })

            current_phase = phase
            start_month = month
            phase_count = 1

        else:
            phase_count += 1

        previous_month = month

    eras.append({
        "phase": current_phase,
        "start": start_month,
        "end": previous_month
    })

    return eras


def print_tree(eras):

    print("\nBitcoin Evolution Tree")
    print("--------------------------------------------------")

    for era in eras:

        print(
            f"{era['start']} → {era['end']}   |   {era['phase']}"
        )


def main():

    eras = build_tree()

    print_tree(eras)


if __name__ == "__main__":
    main()
