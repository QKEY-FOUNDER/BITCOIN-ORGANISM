import csv
import numpy as np
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"
PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"


def load_series():

    pressures = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            pressures.append(float(row["pressure"]))

    return pressures


def rolling_variance(series, window=12):

    variances = []

    for i in range(len(series)):

        if i < window:

            variances.append(None)

        else:

            segment = series[i-window:i]

            variances.append(np.var(segment))

    return variances


def rolling_autocorrelation(series, window=12):

    ac = []

    for i in range(len(series)):

        if i < window:

            ac.append(None)

        else:

            segment = series[i-window:i]

            x = segment[:-1]
            y = segment[1:]

            corr = np.corrcoef(x, y)[0,1]

            ac.append(corr)

    return ac


def main():

    print("\nBitcoin Organism — Early Warning Engine")
    print("--------------------------------------------------")

    pressures = load_series()

    variance = rolling_variance(pressures)

    autocorr = rolling_autocorrelation(pressures)

    latest_var = variance[-1]
    latest_ac = autocorr[-1]

    print("Latest variance:", round(latest_var,4))
    print("Latest autocorrelation:", round(latest_ac,4))
    print("")

    warning_score = 0

    if latest_var > 0.8:
        warning_score += 1

    if latest_ac > 0.6:
        warning_score += 1

    if warning_score == 0:

        print("Early Warning Signal:")
        print("System stable")

    elif warning_score == 1:

        print("Early Warning Signal:")
        print("Potential regime tension")

    else:

        print("Early Warning Signal:")
        print("Approaching critical transition")


if __name__ == "__main__":
    main()
