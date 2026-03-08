import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"


def load_series():

    months = []
    pressures = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:

            months.append(r["month"])
            pressures.append(float(r["pressure"]))

    return months, pressures


def detect_eras(months, pressures):

    eras = []

    current_era = None
    start_month = None

    for m,p in zip(months, pressures):

        if p > 3:

            era = "Monetary Layer"

        elif p > 2.2:

            era = "Institutional Expansion"

        elif p > 1.6:

            era = "Global Discovery"

        elif p > 1.0:

            era = "Early Network"

        else:

            era = "Genesis"

        if current_era is None:

            current_era = era
            start_month = m

        elif era != current_era:

            eras.append((current_era, start_month, m))

            current_era = era
            start_month = m

    eras.append((current_era, start_month, months[-1]))

    return eras


def main():

    print("\nBitcoin Organism — Evolution Era Detector")
    print("--------------------------------------------------")

    months, pressures = load_series()

    eras = detect_eras(months, pressures)

    print("Detected evolutionary eras:\n")

    for era, start, end in eras:

        print(era)
        print(start,"→",end)
        print("")


if __name__ == "__main__":
    main()
