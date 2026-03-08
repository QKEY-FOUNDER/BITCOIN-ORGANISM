import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"
PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"
OUTPUT_PATH = DATA_PATH / "bitcoin_evolution_climate.png"


def load_series():
    months = []
    pressures = []

    with open(PRESSURE_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            months.append(row["month"])
            pressures.append(float(row["pressure"]))

    return months, pressures


def moving_average(series, window=6):
    ma = []

    for i in range(len(series)):
        if i < window:
            ma.append(None)
        else:
            window_slice = series[i-window:i]
            ma.append(sum(window_slice) / window)

    return ma


def detect_climate_shifts(pressures, ma, threshold=0.6):
    shifts = []

    for i in range(1, len(ma)):
        if ma[i] is None or ma[i-1] is None:
            continue

        delta = ma[i] - ma[i-1]

        if abs(delta) > threshold:
            shifts.append((i, pressures[i], delta))

    return shifts


def main():

    print("\nBitcoin Organism — Evolution Climate Engine")
    print("--------------------------------------------------")

    months, pressures = load_series()

    ma = moving_average(pressures, window=6)

    shifts = detect_climate_shifts(pressures, ma)

    print("Detected climate transitions:")
    print("")

    for idx, p, delta in shifts:
        print(months[idx], "pressure:", round(p,3), "shift:", round(delta,3))

    plt.figure(figsize=(16,6))

    plt.plot(pressures, linewidth=1, label="Pressure")
    plt.plot(ma, linewidth=2, label="Climate Trend")

    for idx, p, delta in shifts:
        plt.scatter(idx, p, s=80)

    plt.axhline(1.5, linestyle="--")
    plt.axhline(2.2, linestyle="--")
    plt.axhline(3.0, linestyle="--")

    plt.title("Bitcoin Organism — Evolution Climate Map")
    plt.xlabel("Time")
    plt.ylabel("Evolution Pressure")

    plt.legend()

    plt.tight_layout()

    plt.savefig(OUTPUT_PATH)

    print("")
    print("Climate map saved:")
    print(OUTPUT_PATH)

    import os
    os.system(f"open {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
