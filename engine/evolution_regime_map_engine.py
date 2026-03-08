import csv
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
OUTPUT_FILE = DATA_PATH / "evolution_regime_map.png"


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def regime_color(regime):

    colors = {
        "Equilibrium": "#4CAF50",
        "Compression": "#FFC107",
        "Expansion": "#2196F3",
        "Instability": "#F44336"
    }

    return colors[regime]


def load_series():

    months = []
    regimes = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:

            month = r["month"]
            pressure = float(r["pressure"])

            regime = classify_regime(pressure)

            months.append(month)
            regimes.append(regime)

    return months, regimes


def build_map(months, regimes):

    colors = [regime_color(r) for r in regimes]

    plt.figure(figsize=(14,3))

    plt.scatter(range(len(months)), [1]*len(months), c=colors, s=40)

    plt.yticks([])

    plt.title("Bitcoin Organism - Evolution Regime Map")

    plt.xlabel("Time (months)")

    plt.savefig(OUTPUT_FILE, bbox_inches="tight")


def main():

    print("\nBitcoin Organism - Evolution Regime Map")
    print("--------------------------------------------------")

    months, regimes = load_series()

    build_map(months, regimes)

    print("Months analysed:", len(months))

    print("Regime map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
