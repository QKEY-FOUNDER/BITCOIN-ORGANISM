import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
TRANSITION_FILE = DATA_PATH / "critical_transition_state.json"
BARRIER_FILE = DATA_PATH / "barrier_energy_state.json"
NAVIGATION_FILE = DATA_PATH / "evolution_navigation_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_weather_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Evolution Weather Engine")
    print("--------------------------------------------------")

    energy_state = load_json(ENERGY_FILE)
    transition_state = load_json(TRANSITION_FILE)
    barrier_state = load_json(BARRIER_FILE)
    navigation_state = load_json(NAVIGATION_FILE)

    energy = None
    transition_prob = None
    escape_ratio = None
    dominant_direction = None

    if energy_state:
        energy = energy_state.get("energy_metrics", {}).get("evolution_energy")

    if transition_state:
        transition_prob = transition_state.get("transition_probability")

    if barrier_state:
        escape_ratio = barrier_state.get("escape_energy_ratio")

    if navigation_state:
        dominant_direction = navigation_state.get("dominant_direction")

    print("")
    print("Evolution energy:", energy)
    print("Transition probability:", transition_prob)
    print("Barrier escape ratio:", escape_ratio)
    print("Dominant direction:", dominant_direction)

    weather = "Unknown"

    if energy < 1:
        weather = "Calm Basin"

    elif energy >= 1 and transition_prob < 0.2:
        weather = "Stable Basin"

    elif energy >= 1.5 and transition_prob >= 0.2 and transition_prob < 0.4:
        weather = "Structural Tension"

    elif energy >= 1.8 and escape_ratio and escape_ratio > 2:
        weather = "Escape Dynamics"

    elif transition_prob and transition_prob > 0.5:
        weather = "Phase Transition Storm"

    print("")
    print("Evolutionary weather:")
    print(weather)

    output = {
        "energy": energy,
        "transition_probability": transition_prob,
        "escape_ratio": escape_ratio,
        "dominant_direction": dominant_direction,
        "evolution_weather": weather
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Weather state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
