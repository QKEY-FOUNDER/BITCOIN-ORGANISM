import os
import json
import csv
import math
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_PATH / "data" / "organism_metrics"
PRESSURE_CSV = BASE_PATH / "data" / "evolution_pressure.csv"


# --------------------------------------------------
# Calcular pressão evolutiva
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

    return round(pressure, 6)


# --------------------------------------------------
# Classificação de regime
# --------------------------------------------------

def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


# --------------------------------------------------
# Carregar métricas (filtrando anos iniciais)
# --------------------------------------------------

def load_metrics():

    records = []

    for f in os.listdir(METRICS_PATH):

        if not f.startswith("bitcoin_"):
            continue

        if not f.endswith("_metrics.json"):
            continue

        if "FULL" in f:
            continue

        year = int(f.split("_")[1])

        # Ignorar era inicial do Bitcoin
        if year < 2016:
            continue

        with open(METRICS_PATH / f) as j:
            metrics = json.load(j)

        if metrics["structural_tension"] is None:
            continue

        month = f.replace("_metrics.json", "")

        records.append((month, metrics))

    records.sort()

    return records


# --------------------------------------------------
# Série de pressão
# --------------------------------------------------

def load_pressure_series():

    series = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            series.append(
                (row["month"], float(row["pressure"]))
            )

    return series


# --------------------------------------------------
# Normalização
# --------------------------------------------------

def normalize(v, scale):

    if scale == 0:
        return 0

    return v / scale


# --------------------------------------------------
# Distância fisiológica melhorada
# --------------------------------------------------

def distance(m1, m2):

    d = 0

    d += (normalize(m1["structural_tension"], 0.5) - normalize(m2["structural_tension"], 0.5)) ** 2
    d += (normalize(m1["volatility_resonance"], 1.0) - normalize(m2["volatility_resonance"], 1.0)) ** 2
    d += (normalize(m1["heartbeat_variability"], 0.05) - normalize(m2["heartbeat_variability"], 0.05)) ** 2
    d += (normalize(m1["arrhythmia_index"], 0.1) - normalize(m2["arrhythmia_index"], 0.1)) ** 2

    return math.sqrt(d)


# --------------------------------------------------
# Encontrar pressão futura
# --------------------------------------------------

def future_pressure(month, pressure_series, horizon):

    months = [m for m, _ in pressure_series]

    if month not in months:
        return None

    i = months.index(month)

    if i + horizon >= len(pressure_series):
        return None

    return pressure_series[i + horizon][1]


# --------------------------------------------------
# Motor principal
# --------------------------------------------------

def main():

    print("\nBitcoin Organism — Evolution Scenarios V2")
    print("--------------------------------------------------")

    metrics = load_metrics()
    pressure_series = load_pressure_series()

    current_month, current_metrics = metrics[-1]

    print("Current state:", current_month)

    distances = []

    for m, data in metrics[:-1]:

        d = distance(current_metrics, data)

        distances.append((m, d))

    distances.sort()

    top = distances[:10]

    print("\nTop analogous states:")

    for m, d in top:
        print(m, "distance:", round(d, 4))

    horizons = [3, 6, 12]

    scenario_results = {h: [] for h in horizons}

    for month, dist in top:

        for h in horizons:

            fp = future_pressure(month, pressure_series, h)

            if fp is None:
                continue

            regime = classify_regime(fp)

            scenario_results[h].append(regime)

    print("\nScenario probabilities:\n")

    for h in horizons:

        outcomes = scenario_results[h]

        if len(outcomes) == 0:
            continue

        counts = {}

        for o in outcomes:
            counts[o] = counts.get(o, 0) + 1

        print(str(h) + " months ahead:")

        total = len(outcomes)

        for regime, c in counts.items():

            p = c / total

            print(regime, "→", round(p, 3))

        print("")


if __name__ == "__main__":
    main()
