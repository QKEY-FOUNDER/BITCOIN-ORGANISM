import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"
BRAIN_FILE = DATA_PATH / "evolution_brain_state.json"
OBS_FILE = DATA_PATH / "evolution_observatory_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_genome.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def main():

    print("")
    print("Bitcoin Organism — Evolution Genome Engine")
    print("--------------------------------------------------")

    attractor = load_json(ATTRACTOR_FILE)
    brain = load_json(BRAIN_FILE)
    observatory = load_json(OBS_FILE)

    attractor_levels = None
    current_attractor = None

    if attractor:
        attractor_levels = attractor.get("attractor_levels")
        current_attractor = attractor.get("current_attractor")

    adaptive_weight = None
    model_state = None

    if brain:
        adaptive_weight = brain.get("adaptive_weight")
        model_state = brain.get("model_state")

    evolution_stage = None

    if observatory:
        evolution_stage = observatory.get("evolution_stage")

    genome = {
        "organism": "BITCOIN-ORGANISM",
        "genome_version": "1.0",
        "structural_genes": {
            "attractor_levels": attractor_levels,
            "current_attractor": current_attractor
        },
        "adaptive_genes": {
            "adaptive_weight": adaptive_weight,
            "model_state": model_state
        },
        "evolution_state": {
            "stage": evolution_stage
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(genome, f, indent=2)

    print("")
    print("Genome generated")
    print("Genome file:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
