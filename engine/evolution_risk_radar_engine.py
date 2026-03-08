import csv
import json
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
TRANSITION_FILE = DATA_PATH / "evolution_phase_transition.json"


def load_pressure():

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        rows = list(reader)

    pressures = [float(r["pressure"]) for r in rows]

    return pressures


def load_transition():

    if not TRANSITION_FILE.exists():
        return 0

    with open(TRANSITION_FILE) as f:

        data = json.load(f)

    return data.get("transition_probability", 0)


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


def compute_risk(pressure, transition, variance, autocorr):

    score = 0

    if pressure > 3:
        score += 2

    if transition > 0.5:
        score += 2

    if variance > 0.8:
        score += 1

    if autocorr > 0.6:
        score += 1

    if score >= 4:
        return "Critical Risk"

    if score >= 2:
        return "Elevated Risk"

    return "Low Risk"


def main():

    print("\nBitcoin Organism - Evolution Risk Radar")
    print("--------------------------------------------------")

    pressures = load_pressure()

    current_pressure = pressures[-1]

    transition = load_transition()

    window = pressures[-24:]

    variance = compute_variance(window)

    autocorr = compute_autocorrelation(window)

    risk = compute_risk(
        current_pressure,
        transition,
        variance,
        autocorr
    )

    print("Current pressure:", round(current_pressure,3))
    print("Transition probability:", round(transition,3))
    print("Variance:", round(variance,3))
    print("Autocorrelation:", round(autocorr,3))

    print("\nEvolution risk level:")
    print(risk)


if __name__ == "__main__":
    main()
