import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
ATTRACTOR_FILE = DATA_PATH / "evolution_attractor_state.json"

OUTPUT_FILE = DATA_PATH / "evolution_observatory_map.png"


def load_attractors():
    try:
        with open(ATTRACTOR_FILE) as f:
            data = json.load(f)
            return data.get("attractor_levels", [])
    except:
        return []


def main():

    print("")
    print("Bitcoin Organism — Evolution Observatory Map")
    print("--------------------------------------------------")

    df = pd.read_csv(PRESSURE_FILE)

    months = df["month"]
    pressure = df["pressure"]

    attractors = load_attractors()

    plt.figure(figsize=(14,7))

    plt.plot(months, pressure, linewidth=2)

    for level in attractors:
        plt.axhline(level, linestyle="--")

    current_pressure = pressure.iloc[-1]

    plt.scatter(months.iloc[-1], current_pressure, s=120)

    plt.title("Bitcoin Organism Evolution Map")
    plt.xlabel("Evolution Timeline")
    plt.ylabel("Evolution Pressure")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE)

    print("")
    print("Observatory map saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
