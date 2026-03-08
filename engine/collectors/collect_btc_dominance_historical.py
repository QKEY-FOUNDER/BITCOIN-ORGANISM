import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import time

print("📈 BACKFILL BTC DOMINANCE — RATE LIMIT SAFE")

BASE_PATH = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_PATH / "data/raw/dominance"
RAW_DIR.mkdir(parents=True, exist_ok=True)

start_date = datetime(2026, 2, 6)
end_date   = datetime(2026, 2, 19)

url = "https://api.coingecko.com/api/v3/global"

def safe_request(max_retries=5):
    delay = 5
    for attempt in range(max_retries):
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            return response

        if response.status_code == 429:
            print(f"⏳ Rate limit detectado. Aguardar {delay}s...")
            time.sleep(delay)
            delay *= 2
            continue

        print(f"⚠️ Status inesperado: {response.status_code}")
        time.sleep(delay)

    return None

current = start_date

while current <= end_date:

    date_str = current.date().isoformat()
    out_file = RAW_DIR / f"btc_dominance_{date_str}.csv"

    if out_file.exists():
        print(f"⚠️ Já existe: {date_str}")
        current += timedelta(days=1)
        continue

    response = safe_request()

    if response is None:
        print(f"❌ Falha definitiva em {date_str}")
        break

    data = response.json().get("data", {})
    dominance = data.get("market_cap_percentage", {}).get("btc")

    if dominance is None:
        print(f"❌ Dominance ausente em {date_str}")
        break

    df = pd.DataFrame([{
        "Date": date_str,
        "DominanceBTC": round(float(dominance), 4)
    }])

    df.to_csv(out_file, index=False)
    print(f"✅ Criado: {date_str}")

    time.sleep(3)  # delay normal entre chamadas
    current += timedelta(days=1)

print("🧬 BACKFILL CONCLUÍDO")
