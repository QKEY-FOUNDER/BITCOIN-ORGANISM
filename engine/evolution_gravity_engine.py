import json
import numpy as np
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_gravity_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def compute_gravity(current_pressure, attractors, energy):

    forces = []

    for a in attractors:

        distance = abs(current_pressure - a) + 0.001

        gravity = energy / (distance ** 2)

        forces.append({
            "attractor_level": a,
            "distance": distance,
            "gravity_force": gravity
        })

    return forces


def main():

    print("")
    print("Bitcoin Organism — Evolution Gravity Engine")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)

    if not attractor_state:
        print("Attractor state unavailable")
        return

    attractors = attractor_state.get("all_attractors",[])
    current_pressure = attractor_state.get("current_pressure")

    energy = 1

    if energy_state:
        metrics = energy_state.get("energy_metrics",{})
        energy = metrics.get("evolution_energy",1)

    forces = compute_gravity(current_pressure, attractors, energy)

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Evolution energy:", round(energy,4))
    print("")

    print("Attractor gravity forces:")

    for f in forces:

        print(
            "Attractor", round(f["attractor_level"],4),
            "distance:", round(f["distance"],4),
            "gravity:", round(f["gravity_force"],4)
        )

    dominant = max(forces, key=lambda x: x["gravity_force"])

    print("")
    print("Dominant gravitational attractor:")
    print(round(dominant["attractor_level"],4))

    output = {
        "current_pressure": current_pressure,
        "evolution_energy": energy,
        "gravity_forces": forces,
        "dominant_attractor": dominant["attractor_level"]
    }

    with open(OUTPUT_FILE,"w") as f:
        json.dump(output,f)

    print("")
    print("Gravity state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
