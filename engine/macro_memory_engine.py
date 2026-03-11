import pandas as pd
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"
CLIMATE_FILE = BASE_PATH / "data" / "macro_climate_state.json"

OUTPUT_FILE = BASE_PATH / "data" / "macro_memory_state.json"


def load_pressure():

    try:

        df = pd.read_csv(PRESSURE_FILE)

        if "pressure" not in df.columns:
            return None

        return df

    except:

        return None


def load_climate():

    try:

        with open(CLIMATE_FILE) as f:

            data = json.load(f)

        return data.get("macro_climate")

    except:

        return None


def compute_future_changes(series, horizon):

    changes = []

    for i in range(len(series) - horizon):

        current = series.iloc[i]
        future = series.iloc[i + horizon]

        changes.append(future - current)

    return changes


def analyze_conditioned_memory(df):

    pressure = df["pressure"]

    horizons = [3,6,12]

    results = {}

    for h in horizons:

        changes = compute_future_changes(pressure, h)

        if len(changes) == 0:

            results[h] = None

        else:

            results[h] = sum(changes) / len(changes)

    return results


def main():

    print("")
    print("Bitcoin Organism — Contextual Macro Memory Engine")
    print("--------------------------------------------------")

    df = load_pressure()
    climate = load_climate()

    if df is None:

        print("Pressure data unavailable")
        return

    memory = analyze_conditioned_memory(df)

    print("Current macro climate:", climate)
    print("")
    print("Conditioned future pressure expectation:")

    for k,v in memory.items():

        if v is not None:
            print(k,"months:",round(v,4))
        else:
            print(k,"months: insufficient data")

    output = {

        "macro_climate": climate,
        "conditioned_pressure_expectation": memory

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Macro contextual memory saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
