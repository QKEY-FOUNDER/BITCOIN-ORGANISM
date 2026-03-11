import json
import csv
from datetime import datetime
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

CONTROL_FILES = {
    "observatory": "evolution_observatory_state.json",
    "pulse": "evolution_pulse_state.json",
    "energy": "evolution_energy_state.json",
    "macro": "macro_climate_state.json",
    "attractor": "evolution_attractor_state.json"
}

LIFE_LOG = DATA_PATH / "organism_life_log.csv"


def load_json(file_name):
    path = DATA_PATH / file_name
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Life Cycle Engine")
    print("--------------------------------------------------")

    data = {k: load_json(v) for k, v in CONTROL_FILES.items()}

    timestamp = datetime.utcnow().isoformat()

    stage = None
    if data["observatory"]:
        stage = data["observatory"].get("evolution_stage")

    pressure = None
    velocity = None
    pulse_state = None

    if data["pulse"]:
        pressure = data["pulse"].get("current_pressure")
        velocity = data["pulse"].get("velocity")
        pulse_state = data["pulse"].get("pulse_state")

    energy = None
    if data["energy"]:
        energy = data["energy"].get("energy_metrics", {}).get("evolution_energy")

    macro = None
    if data["macro"]:
        macro = data["macro"].get("macro_climate")

    attractor = None
    if data["attractor"]:
        attractor = data["attractor"].get("current_attractor")

    row = [
        timestamp,
        stage,
        pressure,
        velocity,
        energy,
        pulse_state,
        macro,
        attractor
    ]

    header = [
        "timestamp",
        "evolution_stage",
        "pressure",
        "velocity",
        "energy",
        "pulse_state",
        "macro_climate",
        "dominant_attractor"
    ]

    file_exists = LIFE_LOG.exists()

    with open(LIFE_LOG, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(header)

        writer.writerow(row)

    print("")
    print("Life event recorded")
    print("Log file:")
    print(LIFE_LOG)


if __name__ == "__main__":
    main()
