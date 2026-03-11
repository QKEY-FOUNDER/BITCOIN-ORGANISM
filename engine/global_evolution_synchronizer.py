import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

MACRO_FILE = DATA_PATH / "macro_climate_state.json"
WEATHER_FILE = DATA_PATH / "evolution_weather_state.json"
DECISION_FILE = DATA_PATH / "evolution_decision_state.json"

OUTPUT_FILE = DATA_PATH / "global_evolution_synchronization.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Global Evolution Synchronizer")
    print("--------------------------------------------------")

    macro_state = load_json(MACRO_FILE)
    weather_state = load_json(WEATHER_FILE)
    decision_state = load_json(DECISION_FILE)

    macro_climate = None
    organism_weather = None
    organism_decision = None

    if macro_state:
        macro_climate = macro_state.get("macro_climate")

    if weather_state:
        organism_weather = weather_state.get("evolution_weather")

    if decision_state:
        organism_decision = decision_state.get("strategic_posture")

    print("")
    print("Macro climate:", macro_climate)
    print("Organism weather:", organism_weather)
    print("Organism decision:", organism_decision)

    synchronization = "Unknown"

    if macro_climate == "Risk Expansion Climate" and organism_weather in ["Structural Tension", "Escape Dynamics"]:
        synchronization = "Emerging Expansion Synchronization"

    elif macro_climate == "Risk Expansion Climate" and organism_weather == "Calm Basin":
        synchronization = "Dormant Expansion"

    elif macro_climate == "Risk Compression Climate":
        synchronization = "Macro Headwind Regime"

    elif organism_weather == "Phase Transition Storm":
        synchronization = "High Instability Synchronization"

    else:
        synchronization = "Neutral Synchronization"

    print("")
    print("Global synchronization state:")
    print(synchronization)

    output = {
        "macro_climate": macro_climate,
        "organism_weather": organism_weather,
        "organism_decision": organism_decision,
        "synchronization_state": synchronization
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Synchronization state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
