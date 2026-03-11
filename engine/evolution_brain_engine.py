import json
import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
MEMORY_FILE = DATA_PATH / "macro_memory_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_brain_state.json"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def compute_prediction_error(pressure_series):

    errors = []

    for i in range(1, len(pressure_series)):
        predicted = pressure_series[i-1]
        actual = pressure_series[i]

        error = actual - predicted
        errors.append(abs(error))

    if len(errors) == 0:
        return None

    return sum(errors) / len(errors)


def main():

    print("")
    print("Bitcoin Organism — Evolution Brain Engine")
    print("--------------------------------------------------")

    df = pd.read_csv(PRESSURE_FILE)

    pressure = df["pressure"]

    prediction_error = compute_prediction_error(pressure)

    model_state = "Stable Model"
    adaptive_weight = 1.0

    if prediction_error is not None:

        if prediction_error > 1:
            model_state = "Low Reliability"
            adaptive_weight = 0.7

        elif prediction_error > 0.5:
            model_state = "Moderate Reliability"
            adaptive_weight = 0.9

        else:
            model_state = "High Reliability"
            adaptive_weight = 1.1

    print("")
    print("Mean prediction error:", prediction_error)
    print("Adaptive weight:", adaptive_weight)
    print("Model state:", model_state)

    output = {
        "prediction_error": float(prediction_error) if prediction_error else None,
        "adaptive_weight": adaptive_weight,
        "model_state": model_state
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Brain state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
