import csv
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"


def load_series():

    pressures = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:
            pressures.append(float(r["pressure"]))

    return pressures


def compute_variance(series):

    return statistics.pstdev(series)


def compute_autocorrelation(series):

    n = len(series)

    mean = sum(series) / n

    num = 0
    den = 0

    for i in range(n-1):

        num += (series[i] - mean) * (series[i+1] - mean)

    for i in range(n):

        den += (series[i] - mean) ** 2

    if den == 0:
        return 0

    return num / den


def detect_warning(var, autocorr):

    if var > 0.9 and autocorr > 0.6:
        return "Strong early warning signal"

    if var > 0.7 and autocorr > 0.5:
        return "Moderate early warning signal"

    if var > 0.5:
        return "Weak instability signal"

    return "System stable"


def main():

    print("\nBitcoin Organism - Early Warning Engine")
    print("--------------------------------------------------")

    series = load_series()

    window = series[-24:]

    variance = compute_variance(window)

    autocorr = compute_autocorrelation(window)

    warning = detect_warning(variance, autocorr)

    print("Variance:", round(variance,3))
    print("Autocorrelation:", round(autocorr,3))

    print("\nEarly warning signal:")
    print(warning)


if __name__ == "__main__":
    main()
