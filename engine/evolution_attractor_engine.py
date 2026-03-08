import csv
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"


def load_pressure():

    series = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:
            series.append(float(r["pressure"]))

    return series


def compute_attractor(series):

    mean_pressure = statistics.mean(series)

    median_pressure = statistics.median(series)

    std_pressure = statistics.pstdev(series)

    return mean_pressure, median_pressure, std_pressure


def classify_state(current, attractor):

    if current > attractor + 1:
        return "High Expansion"

    if current < attractor - 1:
        return "Deep Compression"

    return "Near Structural Attractor"


def save_state(current, mean, median, std, classification):

    import json

    report = {
        "current_pressure": current,
        "mean_attractor": mean,
        "median_attractor": median,
        "volatility_band": std,
        "system_state": classification
    }

    with open(ATTRACTOR_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism - Evolution Attractor Engine")
    print("--------------------------------------------------")

    series = load_pressure()

    current = series[-1]

    mean, median, std = compute_attractor(series)

    classification = classify_state(current, mean)

    save_state(current, mean, median, std, classification)

    print("Current pressure:", round(current,3))
    print("Mean attractor:", round(mean,3))
    print("Median attractor:", round(median,3))
    print("Volatility band:", round(std,3))
    print("System state:", classification)

    print("Attractor report saved:")
    print(ATTRACTOR_FILE)


if __name__ == "__main__":
    main()
