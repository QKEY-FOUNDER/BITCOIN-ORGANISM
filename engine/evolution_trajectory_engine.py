import csv
import random
import math
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
OUTPUT_FILE = DATA_PATH / "evolution_trajectory_cone.png"


def load_pressure():

    values = []

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        for r in reader:
            values.append(float(r["pressure"]))

    return values


def compute_volatility(series):

    returns = []

    for i in range(1, len(series)):

        change = series[i] - series[i-1]
        returns.append(change)

    mean = sum(returns) / len(returns)

    variance = sum((x-mean)**2 for x in returns) / len(returns)

    return math.sqrt(variance)


def simulate_paths(current_pressure, volatility, months=12, paths=500):

    simulations = []

    for p in range(paths):

        pressure = current_pressure
        path = []

        for m in range(months):

            shock = random.gauss(0, volatility)

            pressure = max(0, pressure + shock)

            path.append(pressure)

        simulations.append(path)

    return simulations


def plot_cone(paths):

    plt.figure(figsize=(10,6))

    for p in paths:
        plt.plot(p, alpha=0.05, color="blue")

    plt.title("Bitcoin Organism Evolution Trajectory Cone")
    plt.xlabel("Months Ahead")
    plt.ylabel("Evolution Pressure")

    plt.savefig(OUTPUT_FILE)


def main():

    print("\nBitcoin Organism - Evolution Trajectory Cone")
    print("--------------------------------------------------")

    series = load_pressure()

    current_pressure = series[-1]

    volatility = compute_volatility(series)

    paths = simulate_paths(current_pressure, volatility)

    plot_cone(paths)

    print("Current pressure:", round(current_pressure,3))
    print("Historical volatility:", round(volatility,3))

    print("Trajectory cone saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
