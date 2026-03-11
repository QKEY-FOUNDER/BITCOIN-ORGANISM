import pandas as pd
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"
OUTPUT_FILE = BASE_PATH / "data" / "evolution_energy_state.json"


def load_pressure():

    try:

        df = pd.read_csv(PRESSURE_FILE)

        if "pressure" not in df.columns:
            return None

        return df["pressure"].dropna().reset_index(drop=True)

    except:

        return None


def compute_energy(series):

    if len(series) < 24:
        return None

    recent = series.tail(12)

    long_term_mean = series.mean()

    volatility = recent.std()

    structural_deviation = abs(recent.iloc[-1] - long_term_mean)

    trend = recent.iloc[-1] - recent.iloc[0]

    energy = volatility + structural_deviation + abs(trend)

    return {

        "volatility": float(volatility),
        "structural_deviation": float(structural_deviation),
        "trend": float(trend),
        "evolution_energy": float(energy)

    }


def classify_energy(energy):

    if energy is None:
        return "Energy data unavailable"

    value = energy["evolution_energy"]

    if value > 1.5:
        return "High Evolution Energy"

    if value > 0.7:
        return "Moderate Evolution Energy"

    return "Low Evolution Energy"


def main():

    print("")
    print("Bitcoin Organism — Evolution Energy Engine")
    print("--------------------------------------------------")

    pressure = load_pressure()

    if pressure is None:

        print("Pressure data unavailable")
        return

    energy_metrics = compute_energy(pressure)

    energy_state = classify_energy(energy_metrics)

    print("Volatility:",round(energy_metrics["volatility"],4))
    print("Structural deviation:",round(energy_metrics["structural_deviation"],4))
    print("Trend:",round(energy_metrics["trend"],4))
    print("")
    print("Evolution energy:",round(energy_metrics["evolution_energy"],4))
    print("Energy state:",energy_state)

    output = {

        "energy_metrics":energy_metrics,
        "energy_state":energy_state

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Evolution energy saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
