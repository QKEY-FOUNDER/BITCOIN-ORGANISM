import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_timeline_map.png"


def load_attractors():
    try:
        with open(ATTRACTOR_FILE) as f:
            data = json.load(f)
            return data.get("attractor_levels", [])
    except:
        return []


def detect_transitions(pressure_series, attractors):
    transitions = []

    for i in range(1, len(pressure_series)):
        p_prev = pressure_series[i-1]
        p_now = pressure_series[i]

        for level in attractors:

            crossed_up = p_prev < level and p_now >= level
            crossed_down = p_prev > level and p_now <= level

            if crossed_up or crossed_down:
                transitions.append((i, level))

    return transitions


def main():

    print("")
    print("Bitcoin Organism — Evolution Timeline Engine")
    print("--------------------------------------------------")

    df = pd.read_csv(PRESSURE_FILE)

    pressure = df["pressure"].values
    months = df["month"]

    attractors = load_attractors()

    transitions = detect_transitions(pressure, attractors)

    plt.figure(figsize=(14,7))

    plt.plot(months, pressure, linewidth=2)

    for level in attractors:
        plt.axhline(level, linestyle="--")

    for t in transitions:
        idx, level = t
        plt.scatter(months.iloc[idx], pressure[idx], s=80)

    plt.title("Bitcoin Organism Evolution Timeline")
    plt.xlabel("Timeline")
    plt.ylabel("Evolution Pressure")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE)

    print("")
    print("Timeline map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
