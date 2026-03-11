import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
TRANSITION_FILE = DATA_PATH / "critical_transition_state.json"

OUTPUT_FILE = DATA_PATH / "regime_path_simulation.png"


def load_json(path):

    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def simulate_paths(current_pressure, attractors, energy, steps=50, simulations=30):

    paths = []

    for _ in range(simulations):

        pos = current_pressure
        trajectory = [pos]

        for _ in range(steps):

            noise = np.random.normal(0,0.05)

            force = 0
            for a in attractors:
                force += -(pos-a)*0.02

            energy_push = np.random.normal(0, energy*0.01)

            pos = pos + force + noise + energy_push

            trajectory.append(pos)

        paths.append(trajectory)

    return np.array(paths)


def main():

    print("")
    print("Bitcoin Organism — Regime Path Simulator")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)
    transition_state = load_json(TRANSITION_FILE)

    if not attractor_state:
        print("Attractor state unavailable")
        return

    attractors = attractor_state.get("all_attractors",[])
    current_pressure = attractor_state.get("current_pressure")

    energy = 1

    if energy_state:
        metrics = energy_state.get("energy_metrics",{})
        energy = metrics.get("evolution_energy",1)

    paths = simulate_paths(current_pressure, attractors, energy)

    plt.figure(figsize=(10,5))

    for p in paths:
        plt.plot(p, alpha=0.3)

    for a in attractors:
        plt.axhline(a, linestyle="--")

    plt.title("Bitcoin Organism Regime Path Simulation")
    plt.xlabel("Simulation Steps")
    plt.ylabel("Evolution Pressure")

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)

    print("")
    print("Simulation map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
