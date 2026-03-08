import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"
PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"
OUTPUT_PATH = DATA_PATH / "bitcoin_evolution_timeline.png"


def load_series():

    months = []
    pressures = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            months.append(row["month"])
            pressures.append(float(row["pressure"]))

    return months, pressures


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def main():

    print("\nBitcoin Organism — Evolution Timeline")
    print("--------------------------------------------------")

    months, pressures = load_series()

    regimes = [classify_regime(p) for p in pressures]

    colors = []

    for r in regimes:

        if r == "Equilibrium":
            colors.append("blue")

        elif r == "Compression":
            colors.append("orange")

        elif r == "Expansion":
            colors.append("green")

        else:
            colors.append("red")

    plt.figure(figsize=(16,6))

    plt.scatter(range(len(pressures)), pressures, c=colors, s=12)

    plt.plot(pressures, linewidth=1)

    plt.axhline(1.5, linestyle="--")
    plt.axhline(2.2, linestyle="--")
    plt.axhline(3.0, linestyle="--")

    plt.title("Bitcoin Organism — Evolution Timeline")
    plt.xlabel("Time")
    plt.ylabel("Evolution Pressure")

    plt.tight_layout()

    plt.savefig(OUTPUT_PATH)

    print("Timeline saved:")
    print(OUTPUT_PATH)

    print("Months analysed:", len(months))

    print("\nOpening timeline...")

    import os
    os.system(f"open {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
