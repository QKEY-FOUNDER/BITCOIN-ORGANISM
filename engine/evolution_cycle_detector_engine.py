import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"


def classify_phase(p):

    if p < 1.3:
        return "Accumulation"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Peak"


def load_series():

    months = []
    phases = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:

            month = r["month"]
            pressure = float(r["pressure"])

            phase = classify_phase(pressure)

            months.append(month)
            phases.append(phase)

    return months, phases


def detect_cycle(phases):

    current = phases[-1]

    previous = phases[-2]

    if current == "Expansion" and previous == "Compression":
        return "Early Expansion Cycle"

    if current == "Peak":
        return "Late Cycle / Possible Top"

    if current == "Compression":
        return "Cycle Cooling Phase"

    if current == "Accumulation":
        return "Early Accumulation Phase"

    return "Cycle Stable"


def main():

    print("\nBitcoin Organism - Evolution Cycle Detector")
    print("--------------------------------------------------")

    months, phases = load_series()

    current_month = months[-1]
    current_phase = phases[-1]

    cycle_state = detect_cycle(phases)

    print("Current month:", current_month)
    print("Cycle phase:", current_phase)
    print("Cycle interpretation:", cycle_state)

    print("Total months analysed:", len(months))


if __name__ == "__main__":
    main()
