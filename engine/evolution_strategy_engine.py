import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

INTELLIGENCE_FILE = DATA_PATH / "evolution_intelligence_state.json"
REFLEX_FILE = DATA_PATH / "evolution_reflex_signal.json"
STRATEGY_FILE = DATA_PATH / "evolution_strategy.json"


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def determine_strategy(regime, reflex):

    if reflex in ["Critical Expansion"]:
        return "Risk Defense"

    if reflex in ["Rapid Contraction"]:
        return "Defensive Position"

    if regime == "Expansion":
        return "Expansion Participation"

    if regime == "Compression":
        return "Accumulation Posture"

    if regime == "Equilibrium":
        return "Neutral Observation"

    if regime == "Instability":
        return "Risk Management"

    return "Neutral Observation"


def build_strategy(intelligence, reflex_data):

    regime = "unknown"
    reflex_signal = "unknown"

    if intelligence:
        regime = intelligence.get("regime", "unknown")

    if reflex_data:
        reflex_signal = reflex_data.get("reflex_signal", "unknown")

    strategy = determine_strategy(regime, reflex_signal)

    report = {
        "regime": regime,
        "reflex_signal": reflex_signal,
        "strategy": strategy
    }

    return report


def save_strategy(report):

    with open(STRATEGY_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism - Evolution Strategy Engine")
    print("--------------------------------------------------")

    intelligence = load_json(INTELLIGENCE_FILE)
    reflex = load_json(REFLEX_FILE)

    report = build_strategy(intelligence, reflex)

    save_strategy(report)

    print("Regime:", report["regime"])
    print("Reflex signal:", report["reflex_signal"])
    print("Strategic posture:", report["strategy"])

    print("Strategy saved:")
    print(STRATEGY_FILE)


if __name__ == "__main__":
    main()
