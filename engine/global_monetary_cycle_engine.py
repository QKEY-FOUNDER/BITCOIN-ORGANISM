import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

LIQUIDITY_FILE = DATA_PATH / "global_liquidity_state.json"
MACRO_FILE = DATA_PATH / "macro_environment.json"
PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def load_pressure():

    import csv

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        rows = list(reader)

    return float(rows[-1]["pressure"])


def classify_cycle(liquidity, macro, pressure):

    liquidity_state = "Unknown"
    macro_state = "Unknown"

    if liquidity:
        liquidity_state = liquidity.get("liquidity_state","Unknown")

    if macro:
        macro_state = macro.get("macro_state","Unknown")

    if liquidity_state == "Global Liquidity Expansion":

        if pressure > 2.5:
            return "Liquidity Driven Bull Phase"

        return "Early Liquidity Expansion"

    if liquidity_state == "Global Liquidity Contraction":

        return "Global Liquidity Tightening Phase"

    if macro_state == "High Macro Instability":

        return "Macro Stress Cycle"

    if pressure < 1.5:

        return "Market Dormant Phase"

    return "Neutral Monetary Cycle"


def main():

    print("\nBitcoin Organism — Global Monetary Cycle")
    print("--------------------------------------------------")

    liquidity = load_json(LIQUIDITY_FILE)

    macro = load_json(MACRO_FILE)

    pressure = load_pressure()

    cycle = classify_cycle(liquidity, macro, pressure)

    print("Pressure:", round(pressure,3))

    if liquidity:
        print("Liquidity:", liquidity.get("liquidity_state"))

    if macro:
        print("Macro environment:", macro.get("macro_state"))

    print("\nMonetary cycle phase:")
    print(cycle)


if __name__ == "__main__":
    main()
