import requests
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

FED_BALANCE_API = "https://api.stlouisfed.org/fred/series/observations?series_id=WALCL&api_key=451c78fae7efcff3f7002a107b40bb6e&file_type=json"

DXY_API = "https://api.stlouisfed.org/fred/series/observations?series_id=DTWEXBGS&api_key=451c78fae7efcff3f7002a107b40bb6e&file_type=json"

def get_fed_balance_sheet():
    try:
        r = requests.get(FED_BALANCE_API, timeout=10)
        data = r.json()
        values = []
        for obs in data.get("observations", []):
            v = obs.get("value")
            if v and v != ".":
                values.append(float(v))
        if len(values) < 12:
            return None
        return values
    except:
        return None

def get_dollar_volatility():

    try:

        r = requests.get(DXY_API, timeout=10)
        data = r.json()

        values = []

        for obs in data.get("observations", []):

            v = obs.get("value")

            if v and v != ".":
                values.append(float(v))

        if len(values) < 10:
            return None

        returns = []

        for i in range(1, len(values)):

            r = (values[i] - values[i-1]) / values[i-1]
            returns.append(r)

        return statistics.pstdev(returns)

    except:

        return None

def classify_liquidity(balance_series, dollar_vol):
    if not balance_series:
        return "Liquidity data unavailable"
    if len(balance_series) < 12:
        return "Insufficient liquidity history"
    growth = balance_series[-1] - balance_series[-12]
    if growth > 200000:
        return "Global Liquidity Expansion"
    if growth < -200000:
        return "Global Liquidity Contraction"
    if dollar_vol and dollar_vol > 0.015:
        return "Liquidity Stress Environment"
    return "Neutral Liquidity Environment"

def main():
    print("")
    print("Bitcoin Organism — Global Liquidity Engine")
    print("--------------------------------------------------")
    balance = get_fed_balance_sheet()
    dollar_vol = get_dollar_volatility()
    state = classify_liquidity(balance, dollar_vol)
    if balance:
        latest_balance = balance[-1]
        growth = balance[-1] - balance[-12]
        print("Fed balance sheet latest:", round(latest_balance, 2))
        print("12-month liquidity change:", round(growth, 2))
    else:
        print("Fed balance sheet: unavailable")
    if dollar_vol:
        print("Dollar volatility:", round(dollar_vol, 6))
    else:
        print("Dollar volatility: unavailable")
    print("")
    print("Liquidity regime:")
    print(state)

if __name__ == "__main__":
    main()
