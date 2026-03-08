import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

CSV_PATH = DATA_PATH / "evolution_pressure.csv"
OUTPUT_PATH = DATA_PATH / "bitcoin_evolution_map.png"


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

            m = row["month"]
            p = float(row["pressure"])

            months.append(m)
            pressure.append(p)
            regimes.append(classify_regime(p))

    return months, pressure, regimes


def regime_color(r):

    if r == "Equilibrium":
        return "green"

    if r == "Compression":
        return "blue"

    if r == "Expansion":
        return "orange"

    return "red"


def main():

    print("\nBitcoin Evolution Map")
    print("--------------------------------------------------")

    months, pressure, regimes = load_series()

    colors = [regime_color(r) for r in regimes]

    x = range(len(months))

    plt.figure(figsize=(16,6))

    plt.scatter(x, pressure, c=colors, s=40)

    plt.plot(x, pressure, linewidth=1)

    plt.title("Bitcoin Evolution Pressure Map")
    plt.xlabel("Months since 2010")
    plt.ylabel("Evolution Pressure")

    plt.tight_layout()

    plt.savefig(OUTPUT_PATH)

    print("Map created:", OUTPUT_PATH)
    print("Months analysed:", len(months))


if __name__ == "__main__":
    main()
