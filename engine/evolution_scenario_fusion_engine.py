import csv
import json
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"


def load_pressure():

    series = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:

            month = r["month"]
            pressure = float(r["pressure"])

            series.append((month, pressure))

    return series


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def compute_volatility(series):

    returns = []

    for i in range(1, len(series)):

        change = series[i][1] - series[i-1][1]

        returns.append(change)

    return statistics.pstdev(returns)


def monte_carlo_projection(current, vol):

    import random

    results = []

    for i in range(1000):

        shock = random.gauss(0, vol)

        future = max(0, current + shock)

        results.append(future)

    return statistics.mean(results)


def historical_projection(series):

    pressures = [p for _,p in series]

    return statistics.mean(pressures[-12:])


def main():

    print("\nBitcoin Organism - Scenario Fusion Engine")
    print("--------------------------------------------------")

    series = load_pressure()

    current_pressure = series[-1][1]

    volatility = compute_volatility(series)

    monte_future = monte_carlo_projection(current_pressure, volatility)

    historical_future = historical_projection(series)

    fused_projection = (monte_future + historical_future) / 2

    regime = classify_regime(fused_projection)

    print("Current pressure:", round(current_pressure,3))

    print("\nMonte Carlo projection:", round(monte_future,3))

    print("Historical projection:", round(historical_future,3))

    print("\nFused projection:", round(fused_projection,3))

    print("Projected regime:", regime)


if __name__ == "__main__":
    main()
