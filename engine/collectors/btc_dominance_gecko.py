import csv
import requests
import time
from datetime import datetime, timedelta

# ==============================
# CONFIGURAÇÃO
# ==============================
START_DATE = "2024-10-01"
END_DATE   = "2025-12-31"
OUTPUT_FILE = "btc_dominance_daily_gecko.csv"

COINGECKO_GLOBAL_URL = "https://api.coingecko.com/api/v3/global"

# ==============================
# UTILITÁRIOS
# ==============================
def daterange(start, end):
    cur = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    while cur <= end:
        yield cur.strftime("%Y-%m-%d")
        cur += timedelta(days=1)

# ==============================
# FETCH DOMINÂNCIA BTC
# ==============================
def fetch_btc_dominance():
    while True:
        r = requests.get(COINGECKO_GLOBAL_URL, timeout=20)

        if r.status_code == 200:
            data = r.json()["data"]
            return round(data["market_cap_percentage"]["btc"], 2)

        if r.status_code == 429:
            print("⚠️  Rate limit atingido — a aguardar 60 segundos...")
            time.sleep(60)
            continue

        r.raise_for_status()

# ==============================
# EXECUÇÃO PRINCIPAL
# ==============================
def run():
    rows = []

    for date in daterange(START_DATE, END_DATE):
        print(f"Fetching {date}")
        dominance = fetch_btc_dominance()

        rows.append({
            "date": date,
            "btc_dominance": dominance
        })

        # respeito total pela API pública
        time.sleep(12)

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["date", "btc_dominance"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV criado com sucesso: {OUTPUT_FILE}")

# ==============================
if __name__ == "__main__":
    run()
