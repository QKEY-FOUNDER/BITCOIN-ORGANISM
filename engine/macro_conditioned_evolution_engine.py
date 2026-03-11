import json
import random
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"
CLIMATE_FILE = BASE_PATH / "data" / "macro_climate_state.json"

OUTPUT_FILE = BASE_PATH / "data" / "macro_conditioned_simulation.json"


def load_current_pressure():

    try:

        import pandas as pd

        df = pd.read_csv(PRESSURE_FILE)

        return float(df["pressure"].dropna().iloc[-1])

    except:

        return None


def load_climate():

    try:

        with open(CLIMATE_FILE) as f:

            data = json.load(f)

        return data.get("macro_climate")

    except:

        return None


def simulate_paths(current_pressure, climate, runs=1000):

    results = {

        "expansion":0,
        "compression":0,
        "equilibrium":0

    }

    for _ in range(runs):

        pressure = current_pressure

        for step in range(12):

            if climate == "Risk Expansion Climate":

                drift = random.gauss(0.02,0.1)

            elif climate == "Global Tightening Climate":

                drift = random.gauss(-0.03,0.1)

            else:

                drift = random.gauss(0.0,0.1)

            pressure += drift

        if pressure > current_pressure + 0.5:

            results["expansion"] += 1

        elif pressure < current_pressure - 0.5:

            results["compression"] += 1

        else:

            results["equilibrium"] += 1

    for k in results:

        results[k] = results[k] / runs

    return results


def main():

    print("")
    print("Bitcoin Organism — Macro Conditioned Evolution Engine")
    print("--------------------------------------------------")

    pressure = load_current_pressure()
    climate = load_climate()

    if pressure is None:

        print("Pressure data unavailable")
        return

    print("Current pressure:",round(pressure,4))
    print("Macro climate:",climate)

    probabilities = simulate_paths(pressure, climate)

    print("")
    print("12-month evolution probabilities:")

    for k,v in probabilities.items():

        print(k,"→",round(v,3))

    output = {

        "macro_climate":climate,
        "probabilities":probabilities

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Simulation saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
