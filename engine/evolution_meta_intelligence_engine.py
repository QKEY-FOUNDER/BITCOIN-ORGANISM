import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

CALIBRATION_FILE = DATA_PATH / "evolution_model_calibration.json"
LEARNING_FILE = DATA_PATH / "evolution_learning_report.json"
META_FILE = DATA_PATH / "evolution_meta_intelligence.json"


def load_json(path):

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def evaluate_model(mean_error, adaptive_weight):

    if mean_error is None:
        return "Unknown Model State"

    adjusted_error = mean_error * adaptive_weight

    if adjusted_error < 0.25:
        return "Model Highly Accurate"

    if adjusted_error < 0.6:
        return "Model Reliable"

    if adjusted_error < 1.0:
        return "Model Needs Adjustment"

    return "Model Drift Detected"


def build_meta_state(calibration, learning):

    adaptive_weight = 1.0
    mean_error = None

    if calibration:
        adaptive_weight = calibration.get("adaptive_weight", 1.0)

    if learning:
        mean_error = learning.get("mean_absolute_error")

    state = evaluate_model(mean_error, adaptive_weight)

    report = {
        "mean_error": mean_error,
        "adaptive_weight": adaptive_weight,
        "meta_state": state
    }

    return report


def save_meta(report):

    with open(META_FILE, "w") as f:
        json.dump(report, f, indent=4)


def main():

    print("\nBitcoin Organism - Evolution Meta Intelligence")
    print("--------------------------------------------------")

    calibration = load_json(CALIBRATION_FILE)
    learning = load_json(LEARNING_FILE)

    report = build_meta_state(calibration, learning)

    save_meta(report)

    print("Mean error:", report["mean_error"])
    print("Adaptive weight:", report["adaptive_weight"])
    print("Meta state:", report["meta_state"])

    print("Meta intelligence saved:")
    print(META_FILE)


if __name__ == "__main__":
    main()
