import csv
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
OUTPUT_FILE = DATA_PATH / "bitcoin_evolution_atlas.png"


def load_series():

    months = []
    pressure = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for row in reader:

            months.append(row["month"])
            pressure.append(float(row["pressure"]))

    return months, pressure


def plot_atlas(months, pressure):

    x = range(len(pressure))

    plt.figure(figsize=(16,6))

    plt.plot(x, pressure)

    plt.axhline(1.0)
    plt.axhline(1.6)
    plt.axhline(2.2)
    plt.axhline(3.0)

    plt.title("Bitcoin Evolution Atlas")
    plt.xlabel("Time")
    plt.ylabel("Evolution Pressure")

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE)

    print("\nBitcoin Evolution Atlas")
    print("--------------------------------------------------")
    print("Atlas created:", OUTPUT_FILE)
    print("Months analysed:", len(pressure))


def main():

    months, pressure = load_series()

    plot_atlas(months, pressure)


if __name__ == "__main__":
    main()
