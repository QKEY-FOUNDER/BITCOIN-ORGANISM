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


def compute_recovery_rate(series):

    if len(series) < 2:
        return 0

    recovery = []

    for i in range(1, len(series)):

        delta = abs(series[i] - series[i-1])

        recovery.append(delta)

    return statistics.mean(recovery)


def normalize(value, scale):

    if scale == 0:
        return 0

    return value / scale


def main():

    print("\nBitcoin Organism — Resilience Engine")
    print("--------------------------------------------------")

    records = load_metrics()

    window = records[-24:]

    tension = [m["structural_tension"] for _, m in window]
    vol = [m["volatility_resonance"] for _, m in window]
    hbv = [m["heartbeat_variability"] for _, m in window]

    tension_var = statistics.pstdev(tension)
    vol_var = statistics.pstdev(vol)
    hbv_var = statistics.pstdev(hbv)

    recovery_tension = compute_recovery_rate(tension)
    recovery_vol = compute_recovery_rate(vol)

    instability_score = (
        normalize(tension_var, 0.3) +
        normalize(vol_var, 1.0) +
        normalize(hbv_var, 0.05)
    ) / 3

    recovery_score = (
        normalize(recovery_tension, 0.2) +
        normalize(recovery_vol, 0.5)
    ) / 2

    resilience = max(0, 1 - (instability_score * 0.6 + recovery_score * 0.4))

    print("Variability signals:\n")

    print("structural_tension std:", round(tension_var, 4))
    print("volatility_resonance std:", round(vol_var, 4))
    print("heartbeat_variability std:", round(hbv_var, 4))

    print("\nRecovery dynamics:\n")

    print("tension recovery rate:", round(recovery_tension, 4))
    print("volatility recovery rate:", round(recovery_vol, 4))

    print("\nSystem Resilience Score:")

    print(round(resilience, 3))

    if resilience > 0.7:

        print("\nSystem status: HIGH RESILIENCE")

    elif resilience > 0.4:

        print("\nSystem status: MODERATE RESILIENCE")

    else:

        print("\nSystem status: LOW RESILIENCE")


if __name__ == "__main__":
    main()
