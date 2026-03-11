import pandas as pd
import numpy as np
import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"
OUTPUT_FILE = BASE_PATH / "data" / "critical_transition_state.json"


def load_pressure():

    try:

        df = pd.read_csv(PRESSURE_FILE)

        if "pressure" not in df.columns:
            return None

        return df["pressure"].dropna().reset_index(drop=True)

    except:

        return None


def rolling_metrics(series, window=12):

    volatility = series.rolling(window).std()

    autocorr = series.rolling(window).apply(
        lambda x: pd.Series(x).autocorr(lag=1),
        raw=False
    )

    variance = series.rolling(window).var()

    return volatility, autocorr, variance


def compute_trend(metric):

    metric = metric.dropna()

    if len(metric) < 6:
        return 0

    x = np.arange(len(metric))

    slope = np.polyfit(x, metric, 1)[0]

    return float(slope)


def compute_transition_probability(vol_trend, ac_trend, var_trend):

    score = 0

    if vol_trend > 0:
        score += 1

    if ac_trend > 0:
        score += 1

    if var_trend > 0:
        score += 1

    return score / 3


def main():

    print("")
    print("Bitcoin Organism — Critical Transition Detector")
    print("--------------------------------------------------")

    pressure = load_pressure()

    if pressure is None:

        print("Pressure data unavailable")
        return

    vol, ac, var = rolling_metrics(pressure)

    vol_trend = compute_trend(vol)
    ac_trend = compute_trend(ac)
    var_trend = compute_trend(var)

    probability = compute_transition_probability(
        vol_trend,
        ac_trend,
        var_trend
    )

    print("Trend signals (last 12 months):")
    print("")
    print("volatility trend:",round(vol_trend,4))
    print("autocorrelation trend:",round(ac_trend,4))
    print("variance trend:",round(var_trend,4))
    print("")
    print("Critical transition probability:")
    print(round(probability,3))

    if probability > 0.66:

        signal = "High probability of regime transition"

    elif probability > 0.33:

        signal = "Moderate transition risk"

    else:

        signal = "System relatively stable"

    print("")
    print("Signal:",signal)

    output = {

        "volatility_trend":vol_trend,
        "autocorrelation_trend":ac_trend,
        "variance_trend":var_trend,
        "transition_probability":probability,
        "signal":signal

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Transition state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
