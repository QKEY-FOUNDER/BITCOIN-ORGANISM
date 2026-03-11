import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

SYNC_FILE = DATA_PATH / "global_evolution_synchronization.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
BARRIER_FILE = DATA_PATH / "barrier_energy_state.json"
WEATHER_FILE = DATA_PATH / "evolution_weather_state.json"

OUTPUT_FILE = DATA_PATH / "cycle_genesis_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Cycle Genesis Engine")
    print("--------------------------------------------------")

    sync_state = load_json(SYNC_FILE)
    energy_state = load_json(ENERGY_FILE)
    barrier_state = load_json(BARRIER_FILE)
    weather_state = load_json(WEATHER_FILE)

    synchronization = None
    energy = None
    escape_ratio = None
    weather = None

    if sync_state:
        synchronization = sync_state.get("synchronization_state")

    if energy_state:
        energy = energy_state.get("energy_metrics", {}).get("evolution_energy")

    if barrier_state:
        escape_ratio = barrier_state.get("escape_ratio")

    if weather_state:
        weather = weather_state.get("evolution_weather")

    print("")
    print("Synchronization:", synchronization)
    print("Evolution energy:", energy)
    print("Escape ratio:", escape_ratio)
    print("Evolution weather:", weather)

    cycle_signal = "No Cycle Genesis"
    cycle_probability = 0

    score = 0

    if synchronization == "Emerging Expansion Synchronization":
        score += 1

    if energy and energy > 1.5:
        score += 1

    if escape_ratio and escape_ratio > 2:
        score += 1

    if weather in ["Structural Tension", "Escape Dynamics"]:
        score += 1

    cycle_probability = score / 4

    if score == 4:
        cycle_signal = "Cycle Genesis Detected"

    elif score == 3:
        cycle_signal = "Cycle Formation Phase"

    elif score == 2:
        cycle_signal = "Early Cycle Conditions"

    print("")
    print("Cycle genesis signal:")
    print(cycle_signal)

    print("")
    print("Cycle probability:")
    print(round(cycle_probability, 3))

    output = {
        "synchronization": synchronization,
        "energy": energy,
        "escape_ratio": escape_ratio,
        "weather": weather,
        "cycle_probability": cycle_probability,
        "cycle_signal": cycle_signal
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Cycle genesis state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
