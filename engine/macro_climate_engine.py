import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

MACRO_FILE = BASE_PATH / "data" / "macro_environment_state.json"
BOND_FILE = BASE_PATH / "data" / "bond_market_state.json"
LIQUIDITY_FILE = BASE_PATH / "data" / "liquidity_wave_state.json"

OUTPUT_FILE = BASE_PATH / "data" / "macro_climate_state.json"


def load_json(path):

    try:

        with open(path) as f:
            return json.load(f)

    except:

        return None


def classify_climate(macro_state, bond_state, liquidity_state):

    if macro_state is None or bond_state is None or liquidity_state is None:
        return "Macro data unavailable"

    macro_regime = macro_state.get("macro_environment")
    bond_regime = bond_state.get("bond_regime")
    wave_state = liquidity_state.get("wave_state")

    if "Expansion" in wave_state and "Normal" in bond_regime:
        return "Risk Expansion Climate"

    if "Contraction" in wave_state and "Stress" in bond_regime:
        return "Global Tightening Climate"

    return "Neutral Monetary Climate"


def main():

    print("")
    print("Bitcoin Organism — Macro Climate Engine")
    print("--------------------------------------------------")

    macro_state = load_json(MACRO_FILE)
    bond_state = load_json(BOND_FILE)
    liquidity_state = load_json(LIQUIDITY_FILE)

    climate = classify_climate(macro_state, bond_state, liquidity_state)

    print("Macro environment:", macro_state)
    print("Bond market:", bond_state)
    print("Liquidity wave:", liquidity_state)

    print("")
    print("Detected macro climate:")
    print(climate)

    output = {

        "macro_climate": climate

    }

    with open(OUTPUT_FILE, "w") as f:

        json.dump(output, f)

    print("")
    print("Macro climate saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
