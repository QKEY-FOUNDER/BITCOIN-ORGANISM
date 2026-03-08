import json
import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
TRANSITION_FILE = DATA_PATH / "evolution_phase_transition.json"
ECOSYSTEM_FILE = DATA_PATH / "evolution_ecosystem_state.json"
STRATEGY_FILE = DATA_PATH / "evolution_strategy.json"


def load_pressure():

    with open(PRESSURE_FILE) as f:

        reader = csv.DictReader(f)

        rows = list(reader)

    return float(rows[-1]["pressure"])


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def classify_regime(p):

    if p < 1.5:
        return "Equilibrium"

    if p < 2.2:
        return "Compression"

    if p < 3.0:
        return "Expansion"

    return "Instability"


def interpret_state(regime, ecosystem, transition):

    transition_prob = 0

    if transition:
        transition_prob = transition.get("transition_probability", 0)

    eco_state = "Unknown"

    if ecosystem:
        eco_state = ecosystem.get("ecosystem_state", "Unknown")

    if transition_prob > 0.6:
        return "System approaching structural transition"

    if regime == "Expansion" and eco_state == "Healthy Expansion":
        return "Market expanding with healthy structural conditions"

    if regime == "Compression":
        return "Market energy compressing before potential movement"

    if regime == "Equilibrium":
        return "Market in structural balance"

    if regime == "Instability":
        return "Market entering unstable regime"

    return "Market in transitional evolutionary state"


def main():

    print("\nBitcoin Organism - Evolution Consciousness")
    print("--------------------------------------------------")

    pressure = load_pressure()

    regime = classify_regime(pressure)

    ecosystem = load_json(ECOSYSTEM_FILE)

    transition = load_json(TRANSITION_FILE)

    strategy = load_json(STRATEGY_FILE)

    interpretation = interpret_state(regime, ecosystem, transition)

    print("Pressure:", round(pressure,3))
    print("Regime:", regime)

    if ecosystem:
        print("Ecosystem:", ecosystem.get("ecosystem_state"))

    if transition:
        print("Transition probability:",
              transition.get("transition_probability"))

    if strategy:
        print("Strategy:", strategy.get("strategy"))

    print("\nGlobal interpretation:")
    print(interpretation)


if __name__ == "__main__":
    main()
