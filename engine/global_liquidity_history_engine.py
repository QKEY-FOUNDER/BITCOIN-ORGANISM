import requests
import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

FRED_API_KEY = "451c78fae7efcff3f7002a107b40bb6e"

SERIES = {
    "us_m2": "M2SL",
    "eu_m2": "MYAGM2EZM196N",
    "jp_m2": "MYAGM2JPM189S",
    "cn_m2": "MYAGM2CNM189S"
}

OUTPUT_FILE = BASE_PATH / "data" / "global_m2_history.csv"


def fetch_series(series_id):

    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"

    try:

        r = requests.get(url, timeout=10)
        data = r.json()

        dates = []
        values = []

        for obs in data.get("observations", []):

            v = obs.get("value")

            if v and v != ".":

                dates.append(obs.get("date"))
                values.append(float(v))

        df = pd.DataFrame({
            "date": dates,
            series_id: values
        })

        df["date"] = pd.to_datetime(df["date"])

        return df

    except:

        return None


def merge_series(series_data):

    df = None

    for name, data in series_data.items():

        if data is None:
            continue

        if df is None:
            df = data
        else:
            df = pd.merge(df, data, on="date", how="outer")

    return df


def compute_global_liquidity(df):

    df = df.sort_values("date")

    numeric_cols = df.select_dtypes(include=["float64","int64"]).columns

    df["global_liquidity"] = df[numeric_cols].mean(axis=1)

    df["global_liquidity_growth"] = df["global_liquidity"].pct_change(12)

    return df


def main():

    print("")
    print("Bitcoin Organism — Global Liquidity History Engine")
    print("--------------------------------------------------")

    series_data = {}

    for name, fred_id in SERIES.items():

        print("Fetching:", name)

        data = fetch_series(fred_id)

        series_data[name] = data

    df = merge_series(series_data)

    if df is None:

        print("No liquidity data available")

        return

    df = compute_global_liquidity(df)

    df.to_csv(OUTPUT_FILE, index=False)

    print("")
    print("Global liquidity history saved:")
    print(OUTPUT_FILE)

    print("")
    print("Latest global liquidity growth:")

    latest = df["global_liquidity_growth"].dropna().iloc[-1]

    print(round(latest,4))


if __name__ == "__main__":
    main()
