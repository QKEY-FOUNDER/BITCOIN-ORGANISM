import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
BARRIER_FILE = DATA_PATH / "barrier_energy_state.json"
TRANSITION_FILE = DATA_PATH / "critical_transition_state.json"
ATTRACTOR_FILE = DATA_PATH / "attractor_transition_state.json"

OUTPUT_FILE = DATA_PATH / "phase_transition_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Phase Transition Engine")
    print("--------------------------------------------------")

    energy_state = load_json(ENERGY_FILE)
    barrier_state = load_json(BARRIER_FILE)
    transition_state = load_json(TRANSITION_FILE)
    attractor_state = load_json(ATTRACTOR_FILE)

    energy = None
    escape_ratio = None
    transition_risk = None
    attractor_prob = None

    if energy_state:
        energy = energy_state.get("energy_metrics",{}).get("evolution_energy")

    if barrier_state:
        escape_ratio = barrier_state.get("escape_energy_ratio")

    if transition_state:
        transition_risk = transition_state.get("transition_probability")

    if attractor_state:
        attractor_prob = attractor_state.get("transition_probability")

    print("")
    print("Evolution energy:", energy)
    print("Escape ratio:", escape_ratio)
    print("Transition risk:", transition_risk)
    print("Attractor transition probability:", attractor_prob)

    score = 0

    if energy and energy > 1.5:
        score += 1

    if escape_ratio and escape_ratio > 2:
        score += 1

    if transition_risk and transition_risk > 0.3:
        score += 1

    if attractor_prob and attractor_prob > 0.4:
        score += 1

    if score <= 1:
        regime = "Stable regime"

    elif score == 2:
        regime = "Metastable regime"

    elif score == 3:
        regime = "Transition building"

    else:
        regime = "Phase transition potential"

    print("")
    print("Phase transition diagnosis:")
    print(regime)

    output = {
        "energy": energy,
        "escape_ratio": escape_ratio,
        "transition_risk": transition_risk,
        "attractor_transition_probability": attractor_prob,
        "transition_score": score,
        "phase_state": regime
    }

    with open(OUTPUT_FILE,"w") as f:
        json.dump(output,f)

    print("")
    print("Phase transition state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
