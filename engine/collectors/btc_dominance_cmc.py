import os
import csv
import requests
from datetime import datetime, timedelta

# =========================
# CONFIGURAÇÃO
# =========================

API_KEY = os.getenv("CMC_API_KEY")
if not API_KEY:
    raise RuntimeError("CMC_API_KEY não definida no ambiente")

BASE_URL = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical"

HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY
}

START_DATE = "2024-10-01"
END_DATE   = "2025-12-31"

OUTPUT_FILE = "btc_dominance_daily_cmc.csv"

# =========================
# UTILIDADES
# =========================

def month_ranges(start, end):
    ranges = []
    cur = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    while cur <= end:
        month_start = cur.replace(day=1)

        if cur.month == 12:
            month_end = cur.replace(day=31)
        else:
            next_month = (cur.replace(day=28) + timedelta(days=4)).replace(day=1)
            month_end = next_month - timedelta(days=1)

        ranges.append((
            month_start.strftime("%Y-%m-%d"),
            min(month_end, end).strftime("%Y-%m-%d")
        ))

        cur = month_end + timedelta(days=1)

    return ranges


def to_unix(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())


# =========================
# API
# =========================

def fetch_range(start, end):
    params = {
        "time_start": to_unix(start),
        "time_end": to_unix(end),
        "convert": "USD"
    }

    r = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()

    return r.json()["data"]["quotes"]


# =========================
# MAIN
# =========================

def run():
    rows = []

    for start, end in month_ranges(START_DATE, END_DATE):
        print(f"Fetching {start} → {end}")
        quotes = fetch_range(start, end)

        for q in quotes:
            date = q["timestamp"][:10]
            dominance = q["quote"]["USD"]["btc_dominance"]

            rows.append({
                "Date": date,
                "DominanceBTC": round(dominance, 2)
            })

    rows.sort(key=lambda x: x["Date"])

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "DominanceBTC"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV gerado com sucesso: {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
