import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

META_FILE = DATA_PATH / "evolution_meta_intelligence.json"
REFLEX_FILE = DATA_PATH / "evolution_reflex_signal.json"
TRANSITION_FILE = DATA_PATH / "evolution_phase_transition.json"


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def detect_transition(meta_state, reflex_signal):

    probability = 0.0
    state = "Stable Regime"

    if reflex_signal in ["Critical Expansion", "Deep Compression"]:
        probability = 0.8
        state = "High Transition Risk"

    elif reflex_signal in ["Rapid Expansion", "Rapid Contraction"]:
        probability = 0.5
        state = "Moderate Transition Risk"

    if meta_state == "Model Drift Detected":
        probability += 0.2
        state = "Structural Model Drift"

    probability = min(probability, 1.0)

    return probability, state


def build_transition_state(meta_data, reflex_data):

    meta_state = "Unknown"
    reflex_signal = "Unknown"

    if meta_data:
        meta_state = meta_data.get("meta_state", "Unknown")

    if reflex_data:
        reflex_signal = reflex_data.get("reflex_signal", "Unknown")

    probability, state = detect_transition(meta_state, reflex_signal)

    report = {
        "meta_state": meta_state,
        "reflex_signal": reflex_signal,
        "transition_probability": probability,
        "transition_state": state
    }

    return report


def save_transition(report):

    with open(TRANSITION_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism - Phase Transition Detector")
    print("--------------------------------------------------")

    meta_data = load_json(META_FILE)
    reflex_data = load_json(REFLEX_FILE)

    report = build_transition_state(meta_data, reflex_data)

    save_transition(report)

    print("Meta state:", report["meta_state"])
    print("Reflex signal:", report["reflex_signal"])
    print("Transition probability:", report["transition_probability"])
    print("Transition state:", report["transition_state"])

    print("Transition report saved:")
    print(TRANSITION_FILE)


if __name__ == "__main__":
    main()
