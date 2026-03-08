import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

STRATEGY_FILE = DATA_PATH / "evolution_strategy.json"
REFLEX_FILE = DATA_PATH / "evolution_reflex_signal.json"
CALIBRATION_FILE = DATA_PATH / "evolution_model_calibration.json"


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def compute_calibration(strategy, reflex):

    adjustment = 1.0
    state = "Stable Model"

    if reflex == "Critical Expansion":
        adjustment = 1.2
        state = "Volatility Adaptation"

    elif reflex == "Rapid Expansion":
        adjustment = 1.1
        state = "Momentum Adaptation"

    elif reflex == "Rapid Contraction":
        adjustment = 1.15
        state = "Risk Adaptation"

    elif strategy == "Risk Defense":
        adjustment = 1.25
        state = "Defensive Calibration"

    return adjustment, state


def build_calibration(strategy_data, reflex_data):

    strategy = "unknown"
    reflex = "unknown"

    if strategy_data:
        strategy = strategy_data.get("strategy", "unknown")

    if reflex_data:
        reflex = reflex_data.get("reflex_signal", "unknown")

    adjustment, state = compute_calibration(strategy, reflex)

    report = {
        "strategy": strategy,
        "reflex_signal": reflex,
        "adaptive_weight": adjustment,
        "model_state": state
    }

    return report


def save_calibration(report):

    with open(CALIBRATION_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism - Evolution Self Calibration")
    print("--------------------------------------------------")

    strategy = load_json(STRATEGY_FILE)
    reflex = load_json(REFLEX_FILE)

    report = build_calibration(strategy, reflex)

    save_calibration(report)

    print("Strategy:", report["strategy"])
    print("Reflex:", report["reflex_signal"])
    print("Adaptive weight:", report["adaptive_weight"])
    print("Model state:", report["model_state"])

    print("Calibration saved:")
    print(CALIBRATION_FILE)


if __name__ == "__main__":
    main()
