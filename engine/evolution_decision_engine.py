import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

WEATHER_FILE = DATA_PATH / "evolution_weather_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
TRANSITION_FILE = DATA_PATH / "critical_transition_state.json"
NAVIGATION_FILE = DATA_PATH / "evolution_navigation_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_decision_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Evolution Decision Engine")
    print("--------------------------------------------------")

    weather_state = load_json(WEATHER_FILE)
    energy_state = load_json(ENERGY_FILE)
    transition_state = load_json(TRANSITION_FILE)
    navigation_state = load_json(NAVIGATION_FILE)

    weather = None
    energy = None
    transition_prob = None
    dominant_direction = None

    if weather_state:
        weather = weather_state.get("evolution_weather")

    if energy_state:
        energy = energy_state.get("energy_metrics", {}).get("evolution_energy")

    if transition_state:
        transition_prob = transition_state.get("transition_probability")

    if navigation_state:
        dominant_direction = navigation_state.get("dominant_direction")

    print("")
    print("Evolution weather:", weather)
    print("Evolution energy:", energy)
    print("Transition probability:", transition_prob)
    print("Dominant attractor:", dominant_direction)

    decision = "Observe"

    if weather == "Calm Basin":
        decision = "Observe"

    elif weather == "Stable Basin":
        decision = "Gradual Accumulation"

    elif weather == "Structural Tension":
        decision = "Strategic Patience"

    elif weather == "Escape Dynamics":
        decision = "Prepare for Regime Shift"

    elif weather == "Phase Transition Storm":
        decision = "High Volatility Regime"

    if transition_prob and transition_prob > 0.5:
        decision = "Structural Transition Window"

    print("")
    print("Evolutionary strategic posture:")
    print(decision)

    output = {
        "weather": weather,
        "energy": energy,
        "transition_probability": transition_prob,
        "dominant_direction": dominant_direction,
        "strategic_posture": decision
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Decision state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
