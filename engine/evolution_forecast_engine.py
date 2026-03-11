import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"

OUTPUT_IMAGE = DATA_PATH / "evolution_forecast_paths.png"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def load_pressure():

    pressures = []

    with open(PRESSURE_FILE) as f:

        header = f.readline()

        for line in f:

            p = float(line.strip().split(",")[-1])
            pressures.append(p)

    return pressures


def simulate_paths(current_pressure, attractors, energy, steps=60, paths=200):

    simulations = []

    volatility = 0.05 + (energy * 0.02)

    for _ in range(paths):

        p = current_pressure
        trajectory = [p]

        for _ in range(steps):

            drift = 0

            for a in attractors:

                direction = a - p
                drift += direction * 0.01

            noise = np.random.normal(0, volatility)

            p = p + drift + noise

            trajectory.append(p)

        simulations.append(trajectory)

    return simulations


def main():

    print("")
    print("Bitcoin Organism — Evolution Forecast Engine")
    print("--------------------------------------------------")

    pressures = load_pressure()

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)

    current_pressure = pressures[-1]

    attractors = attractor_state.get("all_attractors")

    energy = energy_state.get("energy_metrics", {}).get("evolution_energy")

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Evolution energy:", round(energy,4))
    print("Attractors:", [round(a,4) for a in attractors])

    simulations = simulate_paths(
        current_pressure,
        attractors,
        energy
    )

    plt.figure(figsize=(12,6))

    for s in simulations:
        plt.plot(s)

    for a in attractors:
        plt.axhline(a, linestyle="--")

    plt.title("Bitcoin Organism — Evolution Forecast Paths")
    plt.xlabel("Simulation Steps")
    plt.ylabel("System Pressure")

    plt.savefig(OUTPUT_IMAGE)

    print("")
    print("Forecast paths saved:")
    print(OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
