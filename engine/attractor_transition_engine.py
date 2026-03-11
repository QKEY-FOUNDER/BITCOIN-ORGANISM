import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
TRANSITION_FILE = DATA_PATH / "critical_transition_state.json"

OUTPUT_FILE = DATA_PATH / "attractor_transition_state.json"


def load_json(path):

    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def compute_transition_probability(energy, transition_risk):

    if energy is None:
        return 0

    base = 0.1

    if energy > 2:
        base += 0.25

    if energy > 3:
        base += 0.25

    if transition_risk is not None:
        base += transition_risk * 0.5

    return min(base,1.0)


def main():

    print("")
    print("Bitcoin Organism — Attractor Transition Engine")
    print("--------------------------------------------------")

    attractor_state = load_json(ATTRACTOR_FILE)
    energy_state = load_json(ENERGY_FILE)
    transition_state = load_json(TRANSITION_FILE)

    if not attractor_state:
        print("Attractor state unavailable")
        return

    current_attractor = attractor_state.get("current_attractor")
    attractor_level = attractor_state.get("attractor_pressure_level")

    energy = None

    if energy_state:
        metrics = energy_state.get("energy_metrics",{})
        energy = metrics.get("evolution_energy")

    transition_risk = None

    if transition_state:
        transition_risk = transition_state.get("transition_probability")

    probability = compute_transition_probability(energy, transition_risk)

    print("")
    print("Current attractor:", current_attractor)
    print("Attractor pressure level:", round(attractor_level,4))

    print("")
    print("Evolution energy:", energy)
    print("Transition risk:", transition_risk)

    print("")
    print("Estimated attractor transition probability:")
    print(round(probability,3))

    if probability > 0.6:
        regime = "High probability of regime shift"
    elif probability > 0.3:
        regime = "Moderate transition potential"
    else:
        regime = "Stable attractor regime"

    print("")
    print("Transition regime:")
    print(regime)

    output = {

        "current_attractor": current_attractor,
        "attractor_pressure_level": attractor_level,
        "evolution_energy": energy,
        "transition_probability": transition_risk,
        "attractor_transition_probability": probability,
        "transition_regime": regime

    }

    with open(OUTPUT_FILE,"w") as f:
        json.dump(output,f)

    print("")
    print("Transition state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
