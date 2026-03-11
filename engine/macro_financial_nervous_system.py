import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

M2_FILE = BASE_PATH / "data" / "global_m2_liquidity.json"
BOND_FILE = BASE_PATH / "data" / "bond_market_state.json"
FED_FILE = BASE_PATH / "data" / "liquidity_state.json"

OUTPUT_FILE = BASE_PATH / "data" / "macro_financial_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def classify_environment(m2, bond, fed):

    if not m2 or not bond or not fed:
        return "Macro Data Incomplete"

    global_growth = m2.get("global_m2_growth")
    credit_spread = bond.get("credit_spread")
    liquidity_regime = fed.get("liquidity_regime")

    if global_growth and global_growth > 0.05 and credit_spread < 2:
        return "Expansion Environment"

    if credit_spread > 3:
        return "Financial Stress Environment"

    if liquidity_regime == "Global Liquidity Contraction":
        return "Financial Stress Environment"

    return "Neutral Environment"


def main():

    print("")
    print("Bitcoin Organism — Macro Financial Nervous System")
    print("--------------------------------------------------")

    m2 = load_json(M2_FILE)
    bond = load_json(BOND_FILE)
    fed = load_json(FED_FILE)

    state = classify_environment(m2, bond, fed)

    print("Global M2:", m2)
    print("Bond Market:", bond)
    print("Fed Liquidity:", fed)

    print("")
    print("Macro Financial State:")
    print(state)

    output = {
        "macro_financial_environment": state
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Macro financial state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
