import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

LEARNING_FILE = DATA_PATH / "evolution_learning_report.json"
ADAPTIVE_FILE = DATA_PATH / "adaptive_model_state.json"


def load_learning():

    with open(LEARNING_FILE) as f:
        report = json.load(f)

    return report


def compute_adjustment(mean_abs_error):

    if mean_abs_error < 0.3:
        adjustment = 1.0
        state = "Stable Model"

    elif mean_abs_error < 0.7:
        adjustment = 1.1
        state = "Moderate Adaptation"

    else:
        adjustment = 1.25
        state = "Strong Adaptation"

    return adjustment, state


def save_model(adjustment, state):

    model = {
        "adaptive_weight": adjustment,
        "model_state": state
    }

    with open(ADAPTIVE_FILE, "w") as f:
        json.dump(model, f, indent=4)


def main():

    print("\nBitcoin Organism — Adaptive Model Engine")
    print("--------------------------------------------------")

    report = load_learning()

    mean_abs_error = report["mean_absolute_error"]

    adjustment, state = compute_adjustment(mean_abs_error)

    save_model(adjustment, state)

    print("Model adaptation computed")

    print("Mean absolute error:", mean_abs_error)
    print("Adaptive weight:", adjustment)
    print("Model state:", state)

    print("Adaptive model saved:")
    print(ADAPTIVE_FILE)


if __name__ == "__main__":
    main()
