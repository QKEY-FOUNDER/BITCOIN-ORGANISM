import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

GRAVITY_FILE = DATA_PATH / "evolution_gravity_state.json"
OUTPUT_FILE = DATA_PATH / "evolution_field_map.png"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Evolution Field Engine")
    print("--------------------------------------------------")

    gravity_state = load_json(GRAVITY_FILE)

    if not gravity_state:
        print("No gravity data available")
        return

    current_pressure = gravity_state.get("current_pressure")

    attractors = []
    forces = []

    for g in gravity_state.get("gravity_forces", []):
        attractors.append(g["attractor_level"])
        forces.append(g["gravity_force"])

    x = np.linspace(0, 4.5, 200)
    field = []

    for p in x:

        total_force = 0

        for a, g in zip(attractors, forces):

            direction = a - p
            distance = abs(direction) + 0.01

            force = g * direction / distance

            total_force += force

        field.append(total_force)

    field = np.array(field)

    plt.figure(figsize=(12,6))

    plt.plot(x, field)

    for a in attractors:
        plt.axvline(a, linestyle="--")

    plt.axvline(current_pressure)

    plt.title("Bitcoin Organism — Evolution Force Field")
    plt.xlabel("System Pressure")
    plt.ylabel("Evolutionary Force")

    plt.savefig(OUTPUT_FILE)

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Attractors:", [round(a,4) for a in attractors])

    print("")
    print("Field map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
