import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

CSV_PATH = DATA_PATH / "evolution_pressure.csv"
OUTPUT_PATH = DATA_PATH / "evolution_cycle_map.png"


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def load_series():

    months = []
    pressure = []
    regimes = []

    with open(CSV_PATH) as f:

        reader = csv.DictReader(f)

        for row in reader:

            p = float(row["pressure"])

            months.append(row["month"])
            pressure.append(p)
            regimes.append(classify_regime(p))

    return months, pressure, regimes


def plot_cycle_map(months, pressure, regimes):

    colors = []

    for r in regimes:

        if r == "Equilibrium":
            colors.append("green")

        elif r == "Compression":
            colors.append("orange")

        elif r == "Expansion":
            colors.append("blue")

        else:
            colors.append("red")

    plt.figure(figsize=(16,6))

    plt.scatter(range(len(pressure)), pressure, c=colors, s=18)

    plt.plot(pressure, alpha=0.3)

    plt.title("Bitcoin Organism — Evolution Cycle Map")
    plt.xlabel("Months (2010 → Present)")
    plt.ylabel("Evolution Pressure")

    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)


def main():

    print("\nBitcoin Organism — Evolution Cycle Map")
    print("--------------------------------------------------")

    months, pressure, regimes = load_series()

    plot_cycle_map(months, pressure, regimes)

    print("Months analysed:", len(months))
    print("Output file:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
