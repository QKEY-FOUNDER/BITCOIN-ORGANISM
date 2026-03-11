import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

CLIMATE_FILE = BASE_PATH / "data" / "macro_climate_state.json"
OUTPUT_FILE = BASE_PATH / "data" / "macro_adaptation_state.json"


def load_climate():

    try:

        with open(CLIMATE_FILE) as f:
            data = json.load(f)

        return data.get("macro_climate")

    except:

        return None


def compute_modifier(climate):

    if climate is None:
        return 0.0

    if climate == "Risk Expansion Climate":
        return -0.05

    if climate == "Global Tightening Climate":
        return 0.10

    return 0.0


def main():

    print("")
    print("Bitcoin Organism — Macro Adaptation Engine")
    print("--------------------------------------------------")

    climate = load_climate()

    modifier = compute_modifier(climate)

    print("Detected macro climate:", climate)
    print("Pressure modifier:", modifier)

    output = {

        "macro_climate": climate,
        "pressure_modifier": modifier

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Macro adaptation state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
