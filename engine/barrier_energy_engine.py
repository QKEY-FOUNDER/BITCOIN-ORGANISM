import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
GRAVITY_FILE = DATA_PATH / "evolution_gravity_state.json"

OUTPUT_FILE = DATA_PATH / "barrier_energy_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def find_next_attractor(current_pressure, attractors):

    higher = [a for a in attractors if a > current_pressure]

    if not higher:
        return None

    return min(higher)


def main():

    print("")
    print("Bitcoin Organism — Barrier Energy Engine")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)
    gravity_state = load_json(GRAVITY_FILE)

    if not attractor_state:
        print("Attractor state unavailable")
        return

    attractors = attractor_state.get("all_attractors",[])
    current_pressure = attractor_state.get("current_pressure")

    energy = None

    if energy_state:
        metrics = energy_state.get("energy_metrics",{})
        energy = metrics.get("evolution_energy")

    next_attractor = find_next_attractor(current_pressure, attractors)

    if next_attractor is None:
        print("No higher attractor detected")
        return

    barrier_height = next_attractor - current_pressure

    escape_ratio = energy / (barrier_height + 0.0001)

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Next attractor:", round(next_attractor,4))
    print("Barrier height:", round(barrier_height,4))

    print("")
    print("Evolution energy:", round(energy,4))
    print("Escape energy ratio:", round(escape_ratio,3))

    if escape_ratio > 5:
        regime = "Barrier easily surmountable"

    elif escape_ratio > 2:
        regime = "Moderate escape potential"

    else:
        regime = "Barrier dominant"

    print("")
    print("Barrier regime:")
    print(regime)

    output = {

        "current_pressure": current_pressure,
        "next_attractor": next_attractor,
        "barrier_height": barrier_height,
        "evolution_energy": energy,
        "escape_energy_ratio": escape_ratio,
        "barrier_regime": regime

    }

    with open(OUTPUT_FILE,"w") as f:
        json.dump(output,f)

    print("")
    print("Barrier energy state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
