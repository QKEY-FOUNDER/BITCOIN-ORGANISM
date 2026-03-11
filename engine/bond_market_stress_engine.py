import requests
import statistics
from pathlib import Path
import json

BASE_PATH = Path(__file__).resolve().parent.parent

API_KEY = "451c78fae7efcff3f7002a107b40bb6e"

YIELD_10Y = f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS10&api_key={API_KEY}&file_type=json"
YIELD_2Y = f"https://api.stlouisfed.org/fred/series/observations?series_id=DGS2&api_key={API_KEY}&file_type=json"
CORP_SPREAD = f"https://api.stlouisfed.org/fred/series/observations?series_id=BAA10YM&api_key={API_KEY}&file_type=json"

def fetch_series(url):
    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        values = []

        for obs in data.get("observations", []):
            v = obs.get("value")

            if v and v != ".":
                values.append(float(v))

        return values

    except:
        return None


def compute_latest(series):
    if not series:
        return None
    return series[-1]


def classify_bond_stress(curve, spread):

    if curve is None or spread is None:
        return "Unknown"

    if curve < 0:
        return "Yield Curve Inversion"

    if spread > 2.5:
        return "Credit Stress"

    return "Normal Bond Market"


def main():

    print("")
    print("Bitcoin Organism — Bond Market Stress Engine")
    print("--------------------------------------------------")

    y10_series = fetch_series(YIELD_10Y)
    y2_series = fetch_series(YIELD_2Y)
    spread_series = fetch_series(CORP_SPREAD)

    y10 = compute_latest(y10_series)
    y2 = compute_latest(y2_series)
    spread = compute_latest(spread_series)

    if y10 is None or y2 is None:
        print("Bond yield data unavailable")
        return

    yield_curve = y10 - y2

    regime = classify_bond_stress(yield_curve, spread)

    print("US 10Y yield:", y10)
    print("US 2Y yield:", y2)
    print("Yield curve (10Y-2Y):", round(yield_curve,4))
    print("Corporate spread:", spread)

    print("")
    print("Bond market regime:", regime)

    output = {
        "yield_10y": y10,
        "yield_2y": y2,
        "yield_curve": yield_curve,
        "credit_spread": spread,
        "bond_regime": regime
    }

    output_path = BASE_PATH / "data" / "bond_market_state.json"

    with open(output_path, "w") as f:
        json.dump(output, f)

    print("")
    print("Bond market state saved:")
    print(output_path)


if __name__ == "__main__":
    main()
