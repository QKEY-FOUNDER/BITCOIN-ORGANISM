import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_regime_atlas.png"


def load_attractors():
    try:
        with open(ATTRACTOR_FILE) as f:
            data = json.load(f)
            return sorted(data.get("attractor_levels", []))
    except:
        return []


def classify_regime(p, attractors):

    if len(attractors) < 4:
        return "unknown"

    a0, a1, a2, a3 = attractors

    if p < a0:
        return "deep_compression"

    elif p < a1:
        return "accumulation"

    elif p < a2:
        return "compression"

    elif p < a3:
        return "expansion"

    else:
        return "instability"


def regime_color(regime):

    colors = {
        "deep_compression": "blue",
        "accumulation": "green",
        "compression": "orange",
        "expansion": "red",
        "instability": "purple"
    }

    return colors.get(regime, "gray")


def main():

    print("")
    print("Bitcoin Organism — Evolution Regime Atlas")
    print("--------------------------------------------------")

    df = pd.read_csv(PRESSURE_FILE)

    months = df["month"]
    pressure = df["pressure"]

    attractors = load_attractors()

    regimes = []

    for p in pressure:
        regimes.append(classify_regime(p, attractors))

    colors = [regime_color(r) for r in regimes]

    plt.figure(figsize=(14,7))

    plt.scatter(months, pressure, c=colors, s=40)

    for level in attractors:
        plt.axhline(level, linestyle="--")

    plt.title("Bitcoin Organism Evolution Regime Atlas")
    plt.xlabel("Timeline")
    plt.ylabel("Evolution Pressure")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE)

    print("")
    print("Regime atlas saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
