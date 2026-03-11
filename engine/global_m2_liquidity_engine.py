import requests
import statistics
from pathlib import Path
import json

BASE_PATH = Path(__file__).resolve().parent.parent

API_KEY = "451c78fae7efcff3f7002a107b40bb6e"

US_M2 = f"https://api.stlouisfed.org/fred/series/observations?series_id=M2SL&api_key={API_KEY}&file_type=json"
EU_M2 = f"https://api.stlouisfed.org/fred/series/observations?series_id=MYAGM2EZM196N&api_key={API_KEY}&file_type=json"
JP_M2 = f"https://api.stlouisfed.org/fred/series/observations?series_id=MYAGM2JPM189S&api_key={API_KEY}&file_type=json"
CN_M2 = f"https://api.stlouisfed.org/fred/series/observations?series_id=MYAGM2CNM189S&api_key={API_KEY}&file_type=json"

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

def compute_growth(series):

    if not series or len(series) < 12:
        return None

    return (series[-1] - series[-12]) / series[-12]

def classify_liquidity(global_growth):

    if global_growth is None:
        return "Unknown"

    if global_growth > 0.08:
        return "Global Liquidity Expansion"

    if global_growth < 0:
        return "Global Liquidity Contraction"

    return "Neutral Liquidity"

def main():

    print("")
    print("Bitcoin Organism — Global M2 Liquidity Engine")
    print("--------------------------------------------------")

    us_series = fetch_series(US_M2)
    eu_series = fetch_series(EU_M2)
    jp_series = fetch_series(JP_M2)
    cn_series = fetch_series(CN_M2)

    us = compute_growth(us_series)
    eu = compute_growth(eu_series)
    jp = compute_growth(jp_series)
    cn = compute_growth(cn_series)

    components = [v for v in [us, eu, jp, cn] if v is not None]

    if len(components) == 0:
        print("No liquidity data available")
        return

    global_growth = statistics.mean(components)

    regime = classify_liquidity(global_growth)

    print("US M2 growth:", us)
    print("EU M2 growth:", eu)
    print("JP M2 growth:", jp)
    print("CN M2 growth:", cn)

    print("")
    print("Global liquidity growth:", round(global_growth,4))
    print("Liquidity regime:", regime)

    output = {
        "us_m2_growth": us,
        "eu_m2_growth": eu,
        "jp_m2_growth": jp,
        "cn_m2_growth": cn,
        "global_m2_growth": global_growth,
        "liquidity_regime": regime
    }

    output_path = BASE_PATH / "data" / "global_m2_liquidity.json"

    with open(output_path, "w") as f:
        json.dump(output, f)

    print("")
    print("Global liquidity data saved:")
    print(output_path)

if __name__ == "__main__":
    main()
