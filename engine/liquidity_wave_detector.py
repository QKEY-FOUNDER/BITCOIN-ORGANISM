import pandas as pd
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

M2_FILE = BASE_PATH / "data" / "global_m2_history.csv"
OUTPUT_FILE = BASE_PATH / "data" / "liquidity_wave_state.json"


def load_liquidity():

    try:

        df = pd.read_csv(M2_FILE)

        if "global_liquidity_growth" not in df.columns:
            return None

        return df["global_liquidity_growth"].dropna().reset_index(drop=True)

    except:

        return None


def compute_acceleration(growth):

    acceleration = growth.diff()

    return acceleration.dropna().reset_index(drop=True)


def detect_wave(acceleration):

    if len(acceleration) < 2:
        return "Insufficient data"

    last = acceleration.iloc[-1]
    prev = acceleration.iloc[-2]

    if prev < 0 and last > 0:
        return "New Liquidity Expansion Wave"

    if prev > 0 and last < 0:
        return "Liquidity Contraction Wave"

    if last > 0:
        return "Ongoing Liquidity Expansion"

    if last < 0:
        return "Ongoing Liquidity Contraction"

    return "Neutral Liquidity"


def main():

    print("")
    print("Bitcoin Organism — Liquidity Wave Detector")
    print("--------------------------------------------------")

    growth = load_liquidity()

    if growth is None:

        print("Liquidity data unavailable")
        return

    acceleration = compute_acceleration(growth)

    state = detect_wave(acceleration)

    latest_growth = growth.iloc[-1]
    latest_acc = acceleration.iloc[-1]

    print("Liquidity growth:", round(latest_growth,4))
    print("Liquidity acceleration:", round(latest_acc,4))
    print("")
    print("Detected liquidity wave:")
    print(state)

    output = {

        "liquidity_growth": float(latest_growth),
        "liquidity_acceleration": float(latest_acc),
        "wave_state": state

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Liquidity wave state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
