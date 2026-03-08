# --------------------------------------------------
# Cycle Evolution Engine
# Bitcoin Organism Historical Evolution
# --------------------------------------------------

import json
import os
from pathlib import Path

from engine.phase_engine import classify_market_phase


BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"


def load_metrics_files():

    files = []

    for f in os.listdir(METRICS_PATH):

        if f.endswith("_metrics.json") and f.startswith("bitcoin_"):
            files.append(f)

    files.sort()

    return files


def compute_delta(current, previous):

    delta = {}

    for k in current:
        if isinstance(current[k], (int, float)):
            delta[k] = current[k] - previous.get(k, 0)

    return delta


def compute_acceleration(delta, previous_delta):

    acc = {}

    acc["volatility_acceleration"] = (
        delta.get("volatility_resonance", 0)
        - previous_delta.get("volatility_resonance", 0)
    )

    acc["geo_entropy_delta"] = delta.get("geo_entropy", 0)

    acc["arrhythmia_slope"] = (
        delta.get("arrhythmia_index", 0)
        - previous_delta.get("arrhythmia_index", 0)
    )

    return acc


def run_cycle_evolution():

    print("\nBitcoin Organism — Evolution Map")
    print("--------------------------------------------------")

    files = load_metrics_files()

    previous_metrics = None
    previous_delta = None
    previous_phase = None
    previous_count = 0

    evolution_map = []

    for file in files:

        path = METRICS_PATH / file

        with open(path) as f:
            metrics = json.load(f)

        if previous_metrics is None:

            delta = {k: 0.0 for k in metrics}
            acceleration = {
                "volatility_acceleration": 0.0,
                "geo_entropy_delta": 0.0,
                "arrhythmia_slope": 0.0,
            }

        else:

            delta = compute_delta(metrics, previous_metrics)
            acceleration = compute_acceleration(delta, previous_delta)

        bundle = {
            "values": metrics,
            "delta": delta,
            "acceleration": acceleration,
        }

        phase, count = classify_market_phase(bundle, previous_phase, previous_count)

        month = file.replace("_metrics.json", "")

        print(f"{month:15} → {phase}")

        evolution_map.append({
            "month": month,
            "phase": phase
        })

        previous_metrics = metrics
        previous_delta = delta
        previous_phase = phase
        previous_count = count

    return evolution_map


if __name__ == "__main__":
    run_cycle_evolution()
