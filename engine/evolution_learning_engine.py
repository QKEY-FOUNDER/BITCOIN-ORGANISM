import csv
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
LEARNING_FILE = DATA_PATH / "evolution_learning_report.json"


def load_pressure():

    rows = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:
            rows.append(r)

    return rows


def compute_trend_error(rows):

    pressures = [float(r["pressure"]) for r in rows]

    errors = []

    for i in range(1, len(pressures)):

        predicted = pressures[i-1]
        actual = pressures[i]

        error = actual - predicted

        errors.append(error)

    mean_error = sum(errors) / len(errors)

    abs_error = sum(abs(e) for e in errors) / len(errors)

    return mean_error, abs_error


def save_learning(mean_error, abs_error):

    report = {
        "mean_prediction_error": round(mean_error, 6),
        "mean_absolute_error": round(abs_error, 6)
    }

    with open(LEARNING_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism — Evolution Learning Engine")
    print("--------------------------------------------------")

    rows = load_pressure()

    mean_error, abs_error = compute_trend_error(rows)

    save_learning(mean_error, abs_error)

    print("Learning report generated")
    print("Mean prediction error:", round(mean_error,6))
    print("Mean absolute error:", round(abs_error,6))
    print("Report saved:", LEARNING_FILE)


if __name__ == "__main__":
    main()
