import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

GLOBAL_M2_FILE = BASE_PATH / "data" / "global_m2_liquidity.json"
BOND_STATE_FILE = BASE_PATH / "data" / "bond_market_state.json"
FED_LIQUIDITY_FILE = BASE_PATH / "data" / "liquidity_state.json"


def load_json(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except:
        return None


def classify_macro_environment(m2_state, bond_state, fed_state):

    signals = []

    if m2_state:
        growth = m2_state.get("global_m2_growth")

        if growth is not None:
            if growth > 0.08:
                signals.append("expansion")
            elif growth < 0:
                signals.append("contraction")
            else:
                signals.append("neutral")

    if bond_state:
        bond_regime = bond_state.get("bond_regime")

        if bond_regime == "Yield Curve Inversion":
            signals.append("stress")

        elif bond_regime == "Credit Stress":
            signals.append("stress")

        else:
            signals.append("normal")

    if fed_state:
        fed_regime = fed_state.get("liquidity_regime")

        if fed_regime == "Global Liquidity Expansion":
            signals.append("expansion")

        elif fed_regime == "Global Liquidity Contraction":
            signals.append("contraction")

        else:
            signals.append("neutral")

    if "stress" in signals or "contraction" in signals:
        return "Financial Stress"

    if signals.count("expansion") >= 2:
        return "Macro Expansion"

    return "Neutral Macro Environment"


def main():

    print("")
    print("Bitcoin Organism — Macro Environment Engine")
    print("--------------------------------------------------")

    m2_state = load_json(GLOBAL_M2_FILE)
    bond_state = load_json(BOND_STATE_FILE)
    fed_state = load_json(FED_LIQUIDITY_FILE)

    macro_state = classify_macro_environment(m2_state, bond_state, fed_state)

    print("Global M2 state:", m2_state)
    print("Bond market state:", bond_state)
    print("Fed liquidity state:", fed_state)

    print("")
    print("Macro environment:", macro_state)

    output = {
        "macro_environment": macro_state
    }

    output_path = BASE_PATH / "data" / "macro_environment_state.json"

    with open(output_path, "w") as f:
        json.dump(output, f)

    print("")
    print("Macro environment saved:")
    print(output_path)


if __name__ == "__main__":
    main()
