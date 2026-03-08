import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🫀 BATIMENTO — Dominance BTC diária (canónico)")

# =========================================================
# PROJECT ROOT (RAIZ REAL DO REPOSITÓRIO)
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# =========================================================
# PATHS CANÓNICOS (NOVA ESTRUTURA)
# =========================================================
DATA_DIR = PROJECT_ROOT / "data" / "market"

RAW_DIR = DATA_DIR / "raw" / "dominance"
RAW_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now(timezone.utc).date()
OUT_FILE = RAW_DIR / f"btc_dominance_{today.isoformat()}_raw.csv"

# =========================================================
# FETCH DATA (CoinGecko)
# =========================================================
url = "https://api.coingecko.com/api/v3/global"
resp = requests.get(url, timeout=30)

if resp.status_code != 200:
    raise RuntimeError("❌ Falha ao obter dados do CoinGecko")

data = resp.json()["data"]
dominance = data["market_cap_percentage"]["btc"]

row = {
    "Date": today.isoformat(),
    "DominanceBTC": round(float(dominance), 4)
}

# =========================================================
# WRITE RAW SNAPSHOT
# =========================================================
df = pd.DataFrame([row])
df.to_csv(OUT_FILE, index=False)

print("✅ Dominance RAW registada com sucesso")
print(f"📅 Date: {row['Date']}")
print(f"📊 DominanceBTC: {row['DominanceBTC']}")
print(f"📁 Ficheiro: {OUT_FILE}")
