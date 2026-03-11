import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

FILES = {
    "macro": "macro_climate_state.json",
    "liquidity": "liquidity_wave_state.json",
    "energy": "evolution_energy_state.json",
    "transition": "critical_transition_state.json",
    "attractor": "evolution_attractor_state.json",
    "barrier": "barrier_energy_state.json",
    "weather": "evolution_weather_state.json",
    "sync": "global_evolution_synchronization.json",
    "cycle": "cycle_genesis_state.json",
    "observatory": "evolution_observatory_state.json",
    "pulse": "evolution_pulse_state.json"
}


def load_json(file_name):
    path = DATA_PATH / file_name
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("BITCOIN ORGANISM — EVOLUTION CONTROL CENTER")
    print("==================================================")

    data = {k: load_json(v) for k, v in FILES.items()}

    macro = data["macro"]
    liquidity = data["liquidity"]
    energy = data["energy"]
    transition = data["transition"]
    attractor = data["attractor"]
    barrier = data["barrier"]
    weather = data["weather"]
    sync = data["sync"]
    cycle = data["cycle"]
    observatory = data["observatory"]
    pulse = data["pulse"]

    macro_climate = macro.get("macro_climate") if macro else None
    liquidity_wave = liquidity.get("wave_state") if liquidity else None

    evolution_energy = None
    if energy:
        evolution_energy = energy.get("energy_metrics", {}).get("evolution_energy")

    transition_risk = None
    if transition:
        transition_risk = transition.get("transition_probability")

    dominant_attractor = None
    if attractor:
        dominant_attractor = attractor.get("current_attractor")

    barrier_ratio = None
    if barrier:
        barrier_ratio = barrier.get("escape_ratio")

    weather_state = weather.get("evolution_weather") if weather else None
    synchronization = sync.get("synchronization_state") if sync else None
    cycle_signal = cycle.get("cycle_signal") if cycle else None
    stage = observatory.get("evolution_stage") if observatory else None

    pulse_state = None
    velocity = None
    acceleration = None
    pressure = None

    if pulse:
        pulse_state = pulse.get("pulse_state")
        velocity = pulse.get("velocity")
        acceleration = pulse.get("acceleration")
        pressure = pulse.get("current_pressure")

    print("")
    print("MACRO ENVIRONMENT")
    print("--------------------------------------------------")
    print("Macro climate:", macro_climate)
    print("Liquidity wave:", liquidity_wave)

    print("")
    print("SYSTEM ENERGY")
    print("--------------------------------------------------")
    print("Evolution energy:", evolution_energy)
    print("Barrier escape ratio:", barrier_ratio)

    print("")
    print("SYSTEM STABILITY")
    print("--------------------------------------------------")
    print("Transition probability:", transition_risk)

    print("")
    print("STRUCTURAL DYNAMICS")
    print("--------------------------------------------------")
    print("Dominant attractor:", dominant_attractor)
    print("Evolution weather:", weather_state)

    print("")
    print("GLOBAL SYNCHRONIZATION")
    print("--------------------------------------------------")
    print("Macro-organism synchronization:", synchronization)

    print("")
    print("CYCLE DIAGNOSTICS")
    print("--------------------------------------------------")
    print("Cycle signal:", cycle_signal)

    print("")
    print("EVOLUTION PULSE")
    print("--------------------------------------------------")
    print("Current pressure:", pressure)
    print("Velocity:", velocity)
    print("Acceleration:", acceleration)
    print("Pulse state:", pulse_state)

    print("")
    print("EVOLUTION STAGE")
    print("--------------------------------------------------")
    print("Current organism stage:", stage)

    print("")
    print("==================================================")
    print("CONTROL CENTER REPORT COMPLETE")
    print("==================================================")


if __name__ == "__main__":
    main()
