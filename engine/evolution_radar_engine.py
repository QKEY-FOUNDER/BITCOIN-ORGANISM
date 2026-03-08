import os
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"


# --------------------------------------------------
# Carregar métricas válidas
# --------------------------------------------------

def load_valid_metrics():

    records = []

    for f in os.listdir(METRICS_PATH):

        if not f.startswith("bitcoin_"):
            continue

        if not f.endswith("_metrics.json"):
            continue

        # ignorar dataset agregado
        if "FULL" in f:
            continue

        with open(METRICS_PATH / f) as j:
            metrics = json.load(j)

        # ignorar meses incompletos
        if metrics["structural_tension"] is None:
            continue

        # ignorar meses fisiologicamente vazios
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


# --------------------------------------------------
# Pressão evolutiva
# --------------------------------------------------

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

    return round(pressure, 3)


# --------------------------------------------------
# Detectar tendência evolutiva
# --------------------------------------------------

def detect_trend(pressures):

    if len(pressures) < 3:
        return "INSUFFICIENT DATA"

    if pressures[-1] > pressures[-2] > pressures[-3]:
        return "ACCELERATING INSTABILITY"

    if pressures[-1] > 2.5:
        return "EARLY STRUCTURAL INSTABILITY"

    return "STABLE REGIME"


# --------------------------------------------------
# Runner principal
# --------------------------------------------------

def main():

    print("\nBitcoin Organism — Evolution Radar")
    print("--------------------------------------------------")

    records = load_valid_metrics()

    if len(records) == 0:
        print("No valid metrics found.")
        return

    # usar os últimos 3 meses válidos
    window = records[-3:]

    pressures = []

    print("Recent Evolution Pressure:")
    print("")

    for month, metrics in window:

        pressure = compute_transition_pressure(metrics)

        pressures.append(pressure)

        print(month, "→", pressure)

    print("")

    trend = detect_trend(pressures)

    print("EVOLUTION TREND →", trend)


if __name__ == "__main__":
    main()
