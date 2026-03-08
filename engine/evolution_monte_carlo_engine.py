import csv
import random
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"
PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"


def load_pressure_series():

    series = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            series.append(
                (row["month"], float(row["pressure"]))
            )

    return series


def compute_volatility(series):

    pressures = [p for _, p in series]

    returns = []

    for i in range(1, len(pressures)):

        r = pressures[i] - pressures[i - 1]

        returns.append(r)

    return statistics.stdev(returns)


def monte_carlo_paths(start_pressure, volatility, months=12, runs=1000):

    paths = []

    for _ in range(runs):

        pressure = start_pressure

        path = []

        for _ in range(months):

            shock = random.gauss(0, volatility)

            pressure = max(0, pressure + shock)

            path.append(pressure)

        paths.append(path)

    return paths


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def analyze_paths(paths):

    final_states = []

    for path in paths:

        final_pressure = path[-1]

        regime = classify_regime(final_pressure)

        final_states.append(regime)

    counts = {}

    for r in final_states:

        counts[r] = counts.get(r, 0) + 1

    total = len(final_states)

    probabilities = {}

    for r, c in counts.items():

        probabilities[r] = c / total

    return probabilities


def main():

    print("\nBitcoin Organism — Monte Carlo Evolution")
    print("--------------------------------------------------")

    series = load_pressure_series()

    current_month, current_pressure = series[-1]

    volatility = compute_volatility(series)

    print("Current state:", current_month)
    print("Current pressure:", round(current_pressure, 3))
    print("Historical volatility:", round(volatility, 3))

    paths = monte_carlo_paths(
        current_pressure,
        volatility,
        months=12,
        runs=2000
    )

    probs = analyze_paths(paths)

    print("\n12-Month Regime Probabilities:\n")

    for regime, p in probs.items():

        print(regime, "→", round(p, 3))


if __name__ == "__main__":
    main()
