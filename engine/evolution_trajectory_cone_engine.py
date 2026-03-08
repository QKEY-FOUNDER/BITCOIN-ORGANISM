import csv
import random
import statistics
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"
PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"
OUTPUT_PATH = DATA_PATH / "evolution_trajectory_cone.png"


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


def monte_carlo_paths(start_pressure, volatility, months=12, runs=500):

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


def compute_cone(paths):

    months = len(paths[0])

    mean_path = []
    upper = []
    lower = []

    for i in range(months):

        values = [p[i] for p in paths]

        mean_path.append(statistics.mean(values))
        upper.append(statistics.quantiles(values, n=10)[8])
        lower.append(statistics.quantiles(values, n=10)[1])

    return mean_path, upper, lower


def plot_cone(history, mean_path, upper, lower):

    pressures = [p for _, p in history]

    months_future = range(len(pressures), len(pressures) + len(mean_path))

    plt.figure(figsize=(10,5))

    plt.plot(pressures, label="Historical Pressure")

    plt.plot(months_future, mean_path, label="Mean Projection")

    plt.fill_between(
        months_future,
        lower,
        upper,
        alpha=0.3,
        label="Trajectory Cone"
    )

    plt.axhline(1.5, linestyle="--")
    plt.axhline(2.2, linestyle="--")
    plt.axhline(3.0, linestyle="--")

    plt.title("Bitcoin Organism — Evolution Trajectory Cone")
    plt.xlabel("Time")
    plt.ylabel("Evolution Pressure")

    plt.legend()

    plt.savefig(OUTPUT_PATH)

    print("\nTrajectory cone saved:")
    print(OUTPUT_PATH)


def main():

    print("\nBitcoin Organism — Evolution Trajectory Cone")
    print("--------------------------------------------------")

    series = load_pressure_series()

    current_month, current_pressure = series[-1]

    volatility = compute_volatility(series)

    print("Current state:", current_month)
    print("Current pressure:", round(current_pressure,3))
    print("Historical volatility:", round(volatility,3))

    paths = monte_carlo_paths(
        current_pressure,
        volatility,
        months=12,
        runs=500
    )

    mean_path, upper, lower = compute_cone(paths)

    plot_cone(series, mean_path, upper, lower)


if __name__ == "__main__":
    main()
