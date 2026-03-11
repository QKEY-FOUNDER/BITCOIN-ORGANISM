import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
GRAVITY_FILE = DATA_PATH / "evolution_gravity_state.json"
BARRIER_FILE = DATA_PATH / "barrier_energy_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_navigation_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Evolution Navigator Engine")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    gravity_state = load_json(GRAVITY_FILE)
    barrier_state = load_json(BARRIER_FILE)

    if not attractor_state:
        print("No attractor data available")
        return

    current_pressure = attractor_state.get("current_pressure")
    attractors = attractor_state.get("all_attractors", [])

    gravity_forces = {}

    if gravity_state:

        raw_forces = gravity_state.get("gravity_forces", [])

        for g in raw_forces:

            level = g.get("attractor_level")
            force = g.get("gravity_force")

            if level is not None:
                gravity_forces[level] = force

    barrier_ratio = None

    if barrier_state:
        barrier_ratio = barrier_state.get("escape_energy_ratio")

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Barrier escape ratio:", barrier_ratio)

    attractor_navigation = {}

    for a in attractors:

        gravity = gravity_forces.get(a, 0)

        if barrier_ratio:
            navigation_force = gravity * barrier_ratio
        else:
            navigation_force = gravity

        attractor_navigation[a] = navigation_force

    sorted_targets = sorted(
        attractor_navigation.items(),
        key=lambda x: x[1],
        reverse=True
    )

    dominant_target = sorted_targets[0][0]

    print("")
    print("Navigation forces toward attractors:")

    for a, force in sorted_targets:
        print("Attractor", round(a,4), "→ navigation force:", round(force,4))

    print("")
    print("Dominant evolutionary direction:")
    print("System tends toward attractor", round(dominant_target,4))

    output = {
        "current_pressure": current_pressure,
        "escape_ratio": barrier_ratio,
        "navigation_forces": attractor_navigation,
        "dominant_direction": dominant_target
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Navigation state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
