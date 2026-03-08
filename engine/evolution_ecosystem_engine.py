import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
RESILIENCE_FILE = DATA_PATH / "evolution_resilience.json"
TRANSITION_FILE = DATA_PATH / "evolution_phase_transition.json"
OUTPUT_FILE = DATA_PATH / "evolution_ecosystem_state.json"


def load_last_pressure():

    import csv

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        rows = list(reader)

    return float(rows[-1]["pressure"])


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def compute_ecosystem_state(pressure, resilience, transition):

    stress = 0
    stability = 0

    if resilience:
        stability = resilience.get("resilience_score", 0)

    if transition:
        stress = transition.get("transition_probability", 0)

    if pressure > 3 and stress > 0.5:
        state = "Overheated Ecosystem"

    elif pressure > 2 and stability > 0.5:
        state = "Healthy Expansion"

    elif pressure < 1.5:
        state = "Dormant Ecosystem"

    elif stress > 0.6:
        state = "Unstable Ecosystem"

    else:
        state = "Balanced Ecosystem"

    return state


def main():

    print("\nBitcoin Organism - Ecosystem State Engine")
    print("--------------------------------------------------")

    pressure = load_last_pressure()

    resilience = load_json(RESILIENCE_FILE)

    transition = load_json(TRANSITION_FILE)

    ecosystem_state = compute_ecosystem_state(
        pressure,
        resilience,
        transition
    )

    report = {
        "pressure": pressure,
        "ecosystem_state": ecosystem_state
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print("Pressure:", round(pressure,3))
    print("Ecosystem state:", ecosystem_state)

    print("Report saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
