import requests
import statistics
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

DOMINANCE_API = "https://api.coingecko.com/api/v3/global"
SP500_API = "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC"
DXY_API = "https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB"


def get_bitcoin_dominance():

    try:

        r = requests.get(DOMINANCE_API)

        data = r.json()

        dominance = data["data"]["market_cap_percentage"]["btc"]

        return dominance

    except:

        return None


def get_market_volatility(api):

    try:

        r = requests.get(api)

        data = r.json()

        prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]

        prices = [p for p in prices if p]

        if len(prices) < 5:
            return None

        returns = []

        for i in range(1, len(prices)):
            r = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(r)

        return statistics.pstdev(returns)

    except:

        return None


def classify_macro_state(dominance, sp500_vol, dxy_vol):

    score = 0

    if dominance and dominance > 50:
        score += 1

    if sp500_vol and sp500_vol > 0.015:
        score += 1

    if dxy_vol and dxy_vol > 0.01:
        score += 1

    if score == 0:
        return "Calm Global Environment"

    if score == 1:
        return "Normal Market Conditions"

    if score == 2:
        return "Rising Global Stress"

    return "High Macro Instability"


def main():

    print("\nBitcoin Organism — Global Macro Sensor")
    print("--------------------------------------------------")

    dominance = get_bitcoin_dominance()

    sp500_vol = get_market_volatility(SP500_API)

    dxy_vol = get_market_volatility(DXY_API)

    state = classify_macro_state(
        dominance,
        sp500_vol,
        dxy_vol
    )

    print("Bitcoin dominance:", dominance)
    print("S&P500 volatility:", sp500_vol)
    print("Dollar index volatility:", dxy_vol)

    print("\nMacro environment:")
    print(state)


if __name__ == "__main__":
    main()
