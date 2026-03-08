import csv
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
REFLEX_FILE = DATA_PATH / "evolution_reflex_signal.json"


def load_pressure():

    rows = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:
            rows.append(r)

    return rows


def compute_reflex(rows):

    pressures = [float(r["pressure"]) for r in rows]

    current = pressures[-1]
    previous = pressures[-2]

    delta = current - previous

    if current > 3:
        signal = "Critical Expansion"

    elif current < 1:
        signal = "Deep Compression"

    elif delta > 0.5:
        signal = "Rapid Expansion"

    elif delta < -0.5:
        signal = "Rapid Contraction"

    else:
        signal = "Stable Evolution"

    return current, delta, signal


def save_reflex(current, delta, signal):

    report = {
        "current_pressure": round(current, 6),
        "pressure_delta": round(delta, 6),
        "reflex_signal": signal
    }

    with open(REFLEX_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism — Evolution Reflex Engine")
    print("--------------------------------------------------")

    rows = load_pressure()

    current, delta, signal = compute_reflex(rows)

    save_reflex(current, delta, signal)

    print("Current pressure:", round(current,6))
    print("Pressure change:", round(delta,6))
    print("Reflex signal:", signal)

    print("Reflex report saved:")
    print(REFLEX_FILE)


if __name__ == "__main__":
    main()
