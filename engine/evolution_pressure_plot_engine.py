import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

CSV_PATH = DATA_PATH / "evolution_pressure.csv"
OUTPUT_PATH = DATA_PATH / "evolution_pressure_plot.png"


# Eventos históricos importantes
EVENTS = {
    "Halving 2012": 29,
    "Halving 2016": 77,
    "Halving 2020": 125,
    "Halving 2024": 173,
    "COVID Crash": 122,
    "FTX Collapse": 149
}


def load_series():

    months = []
    pressure = []

    with open(CSV_PATH) as f:

        reader = csv.DictReader(f)

        for i, row in enumerate(reader):

            months.append(i)
            pressure.append(float(row["pressure"]))

    return months, pressure


def classify_color(p):

    if p < 1.5:
        return "green"

    if p < 2.2:
        return "blue"

    if p < 3.0:
        return "orange"

    return "red"


def main():

    print("\nBitcoin Organism — Evolution Pressure Plot")
    print("--------------------------------------------------")

    months, pressure = load_series()

    colors = [classify_color(p) for p in pressure]

    plt.figure(figsize=(14,6))

    plt.plot(months, pressure, linewidth=2)

    plt.scatter(months, pressure, c=colors, s=25)

    for label, x in EVENTS.items():

        if x < len(months):

            plt.axvline(x=x, linestyle="--", linewidth=1)

            plt.text(
                x,
                max(pressure) * 0.95,
                label,
                rotation=90,
                fontsize=8
            )

    plt.title("Bitcoin Organism — Evolution Pressure (2010 → Present)")
    plt.xlabel("Months since 2010")
    plt.ylabel("Evolution Pressure")

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(OUTPUT_PATH)

    print("Months plotted:", len(months))
    print("Output file:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
