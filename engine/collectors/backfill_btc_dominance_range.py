import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
import time

print("🧠 DOMINANCE STREAM — FORWARD ONLY")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "dominance"
RAW_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now(timezone.utc).date().isoformat()
filename = f"btc_dominance_{today}.csv"
out_file = RAW_DIR / filename

if out_file.exists():
    print("⚠ Já registado hoje — ignorado")
    raise SystemExit(0)

url = "https://api.coingecko.com/api/v3/global"

response = requests.get(url, timeout=20)

if response.status_code != 200:
    raise RuntimeError("❌ Falha API")

data = response.json().get("data", {})
dominance = data.get("market_cap_percentage", {}).get("btc")

if dominance is None:
    raise RuntimeError("❌ Dominance ausente")

df = pd.DataFrame([{
    "Date": today,
    "DominanceBTC": round(float(dominance), 4)
}])

df.to_csv(out_file, index=False)

print(f"✅ Dominance registado para {today}")
