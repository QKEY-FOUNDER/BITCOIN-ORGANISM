import pandas as pd
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"
OUTPUT_FILE = DATA_PATH / "evolution_pulse_state.json"


def main():

    print("")
    print("Bitcoin Organism — Evolution Pulse Engine")
    print("--------------------------------------------------")

    df = pd.read_csv(PRESSURE_FILE)

    pressure = df["pressure"]

    velocity = pressure.diff()
    acceleration = velocity.diff()

    current_pressure = pressure.iloc[-1]
    current_velocity = velocity.iloc[-1]
    current_acceleration = acceleration.iloc[-1]

    print("")
    print("Current pressure:", round(current_pressure,4))
    print("Pressure velocity:", round(current_velocity,4))
    print("Pressure acceleration:", round(current_acceleration,4))

    pulse_state = "Neutral Pulse"

    if current_velocity > 0 and current_acceleration > 0:
        pulse_state = "Accelerating Expansion"

    elif current_velocity > 0 and current_acceleration < 0:
        pulse_state = "Slowing Expansion"

    elif current_velocity < 0 and current_acceleration < 0:
        pulse_state = "Accelerating Compression"

    elif current_velocity < 0 and current_acceleration > 0:
        pulse_state = "Compression Exhaustion"

    print("")
    print("Evolution pulse state:")
    print(pulse_state)

    output = {
        "current_pressure": float(current_pressure),
        "velocity": float(current_velocity),
        "acceleration": float(current_acceleration),
        "pulse_state": pulse_state
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    print("")
    print("Pulse state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
