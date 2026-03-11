import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
OUTPUT_IMAGE = DATA_PATH / "regime_landscape_map.png"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def gaussian(x, mu, sigma):
    return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


def main():

    print("")
    print("Bitcoin Organism — Regime Map Engine")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)

    if not attractor_state:
        print("Attractor data unavailable")
        return

    attractors = attractor_state.get("all_attractors", [])
    current_pressure = attractor_state.get("current_pressure")

    energy = 1

    if energy_state:
        metrics = energy_state.get("energy_metrics", {})
        energy = metrics.get("evolution_energy", 1)

    x = np.linspace(0, 4.5, 1000)
    landscape = np.zeros_like(x)

    for a in attractors:
        landscape -= gaussian(x, a, 0.25)

    landscape = landscape + (x * 0.05)

    plt.figure(figsize=(12,6))

    plt.plot(x, landscape)

    for a in attractors:
        y = -gaussian(a, a, 0.25) + (a * 0.05)
        plt.scatter(a, y)

    current_y = np.interp(current_pressure, x, landscape)
    plt.scatter(current_pressure, current_y)

    plt.title("Bitcoin Organism — Evolutionary Regime Landscape")
    plt.xlabel("System Pressure")
    plt.ylabel("Potential Landscape")

    plt.savefig(OUTPUT_IMAGE)

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Evolution energy:", round(energy,4))
    print("Attractors:", [round(a,4) for a in attractors])

    print("")
    print("Regime landscape map saved:")
    print(OUTPUT_IMAGE)


if __name__ == "__main__":
    main()
