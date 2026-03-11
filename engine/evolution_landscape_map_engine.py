import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_landscape_map.png"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def generate_landscape(attractors):

    x = np.linspace(0,5,500)

    landscape = np.zeros_like(x)

    for a in attractors:
        landscape -= np.exp(-(x-a)**2 / 0.05)

    return x, landscape


def main():

    print("")
    print("Bitcoin Organism — Evolution Landscape Map Engine")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)

    if not attractor_state:
        print("Attractor state unavailable")
        return

    attractors = attractor_state.get("all_attractors",[])
    current_pressure = attractor_state.get("current_pressure")

    energy = None
    if energy_state:
        metrics = energy_state.get("energy_metrics",{})
        energy = metrics.get("evolution_energy")

    x, landscape = generate_landscape(attractors)

    plt.figure(figsize=(10,5))
    plt.plot(x, landscape)

    for a in attractors:
        plt.axvline(a, linestyle="--")

    plt.axvline(current_pressure, linewidth=2)

    plt.title("Bitcoin Organism Evolution Landscape")
    plt.xlabel("Evolution Pressure")
    plt.ylabel("Potential Landscape")

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)

    print("")
    print("Landscape map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
