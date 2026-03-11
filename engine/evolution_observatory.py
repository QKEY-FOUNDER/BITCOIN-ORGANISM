import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

MACRO_FILE = DATA_PATH / "macro_climate_state.json"
LIQUIDITY_FILE = DATA_PATH / "liquidity_wave_state.json"
ENERGY_FILE = DATA_PATH / "evolution_energy_state.json"
TRANSITION_FILE = DATA_PATH / "critical_transition_state.json"
ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
BARRIER_FILE = DATA_PATH / "barrier_energy_state.json"
WEATHER_FILE = DATA_PATH / "evolution_weather_state.json"
SYNC_FILE = DATA_PATH / "global_evolution_synchronization.json"
CYCLE_FILE = DATA_PATH / "cycle_genesis_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_observatory_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Evolution Observatory")
    print("--------------------------------------------------")

    macro = load_json(MACRO_FILE)
    liquidity = load_json(LIQUIDITY_FILE)
    energy = load_json(ENERGY_FILE)
    transition = load_json(TRANSITION_FILE)
    attractor = load_json(ATTRACTOR_FILE)
    barrier = load_json(BARRIER_FILE)
    weather = load_json(WEATHER_FILE)
    sync = load_json(SYNC_FILE)
    cycle = load_json(CYCLE_FILE)

    macro_climate = macro.get("macro_climate") if macro else None
    liquidity_wave = liquidity.get("wave_state") if liquidity else None
    evolution_energy = energy.get("energy_metrics", {}).get("evolution_energy") if energy else None
    transition_risk = transition.get("transition_probability") if transition else None
    dominant_attractor = attractor.get("current_attractor") if attractor else None
    barrier_ratio = barrier.get("escape_ratio") if barrier else None
    weather_state = weather.get("evolution_weather") if weather else None
    synchronization = sync.get("synchronization_state") if sync else None
    cycle_signal = cycle.get("cycle_signal") if cycle else None

    print("")
    print("Macro climate:", macro_climate)
    print("Liquidity wave:", liquidity_wave)
    print("Evolution energy:", evolution_energy)
    print("Transition risk:", transition_risk)
    print("Dominant attractor:", dominant_attractor)
    print("Barrier escape ratio:", barrier_ratio)
    print("Evolution weather:", weather_state)
    print("Synchronization:", synchronization)
    print("Cycle signal:", cycle_signal)

    stage = "Undefined Evolution Stage"

    if cycle_signal == "Cycle Genesis Detected":
        stage = "Cycle Birth Phase"

    elif cycle_signal == "Cycle Formation Phase":
        stage = "Pre-Expansion Phase"

    elif weather_state == "Structural Tension":
        stage = "Accumulation Phase"

    elif weather_state == "Escape Dynamics":
        stage = "Expansion Phase"

    elif weather_state == "Phase Transition Storm":
        stage = "Critical Transition Phase"

    print("")
    print("Detected evolution stage:")
    print(stage)

    output = {
        "macro_climate": macro_climate,
        "liquidity_wave": liquidity_wave,
        "evolution_energy": evolution_energy,
        "transition_risk": transition_risk,
        "dominant_attractor": dominant_attractor,
        "barrier_escape_ratio": barrier_ratio,
        "evolution_weather": weather_state,
        "synchronization": synchronization,
        "cycle_signal": cycle_signal,
        "evolution_stage": stage
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Observatory state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
