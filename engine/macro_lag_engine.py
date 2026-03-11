import pandas as pd
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"
M2_FILE = BASE_PATH / "data" / "global_m2_history.csv"
OUTPUT_FILE = BASE_PATH / "data" / "macro_lag_state.json"


def load_pressure():

    try:

        df = pd.read_csv(PRESSURE_FILE)

        if "pressure" not in df.columns:
            return None

        return df["pressure"].dropna().reset_index(drop=True)

    except:

        return None


def load_liquidity_acceleration():

    try:

        df = pd.read_csv(M2_FILE)

        if "global_liquidity_growth" not in df.columns:
            return None

        growth = df["global_liquidity_growth"].dropna().reset_index(drop=True)

        acceleration = growth.diff()

        acceleration = acceleration.dropna().reset_index(drop=True)

        return acceleration

    except:

        return None


def align_series(liquidity_acc, pressure):

    min_len = min(len(liquidity_acc), len(pressure))

    liquidity_acc = liquidity_acc[-min_len:]
    pressure = pressure[-min_len:]

    return liquidity_acc.reset_index(drop=True), pressure.reset_index(drop=True)


def compute_lag_correlations(liquidity_acc, pressure):

    lags = [0,3,6,9,12]

    results = {}

    for lag in lags:

        shifted = liquidity_acc.shift(lag)

        corr = shifted.corr(pressure)

        results[lag] = float(corr)

    return results


def detect_optimal_lag(correlations):

    best_lag = max(correlations, key=lambda k: abs(correlations[k]))

    return best_lag


def main():

    print("")
    print("Bitcoin Organism — Macro Lag Engine (Liquidity Acceleration)")
    print("--------------------------------------------------")

    pressure = load_pressure()
    liquidity_acc = load_liquidity_acceleration()

    if pressure is None or liquidity_acc is None:

        print("Macro data unavailable")
        return

    liquidity_acc, pressure = align_series(liquidity_acc, pressure)

    correlations = compute_lag_correlations(liquidity_acc, pressure)

    optimal_lag = detect_optimal_lag(correlations)

    print("Lag correlations:")

    for lag,value in correlations.items():

        print(lag,"months:",round(value,4))

    print("")
    print("Optimal macro transmission lag:",optimal_lag,"months")

    output = {

        "lag_correlations":correlations,
        "optimal_lag_months":optimal_lag

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Macro lag state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
