import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

FILES = {
    "strategy": DATA_PATH / "evolution_strategy.json",
    "ecosystem": DATA_PATH / "evolution_ecosystem_state.json",
    "transition": DATA_PATH / "evolution_phase_transition.json",
    "meta": DATA_PATH / "evolution_meta_intelligence.json",
    "attractor": DATA_PATH / "evolution_attractor_state.json"
}


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def main():

    print("\nBITCOIN ORGANISM — INTELLIGENCE DASHBOARD")
    print("==================================================")

    strategy = load_json(FILES["strategy"])
    ecosystem = load_json(FILES["ecosystem"])
    transition = load_json(FILES["transition"])
    meta = load_json(FILES["meta"])
    attractor = load_json(FILES["attractor"])

    print("\nSYSTEM STATE")
    print("--------------------------------------------------")

    if ecosystem:
        print("Ecosystem:", ecosystem.get("ecosystem_state"))

    if strategy:
        print("Strategy:", strategy.get("strategy"))

    print("\nRISK MONITORING")
    print("--------------------------------------------------")

    if transition:
        print("Transition probability:",
              transition.get("transition_probability"))

    if meta:
        print("Model state:", meta.get("meta_state"))

    print("\nSTRUCTURAL DYNAMICS")
    print("--------------------------------------------------")

    if attractor:
        print("Current pressure:",
              attractor.get("current_pressure"))

        print("Structural attractor:",
              attractor.get("mean_attractor"))

        print("Volatility band:",
              attractor.get("volatility_band"))

    print("\nORGANISM STATUS SUMMARY")
    print("--------------------------------------------------")

    if ecosystem and strategy:

        eco = ecosystem.get("ecosystem_state")
        strat = strategy.get("strategy")

        print("Market ecosystem:", eco)
        print("Recommended posture:", strat)

    print("\nDashboard complete.")
    print("==================================================")


if __name__ == "__main__":
    main()
