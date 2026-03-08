import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🫀 BATIMENTO — OHLCV BTC diário (canónico)")

# =========================================================
# PROJECT ROOT (RAIZ REAL DO REPOSITÓRIO)
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# =========================================================
# PATHS CANÓNICOS
# =========================================================
DATA_DIR = PROJECT_ROOT / "data" / "market"

RAW_DIR = DATA_DIR / "raw" / "ohlcv"
RAW_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now(timezone.utc).date()
OUT_FILE = RAW_DIR / f"btc_ohlcv_{today.isoformat()}_raw.csv"

# =========================================================
# FETCH DATA (Binance — candle fechado diário)
# =========================================================
url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",
    "interval": "1d",
    "limit": 2  # último candle fechado
}

resp = requests.get(url, params=params, timeout=30)

if resp.status_code != 200:
    raise RuntimeError("❌ Falha ao obter dados da Binance")

data = resp.json()

if len(data) < 2:
    raise RuntimeError("❌ Dados insuficientes retornados pela Binance")

# O último candle pode estar em formação, usamos o penúltimo
candle = data[-2]

row = {
    "Date": datetime.fromtimestamp(candle[0] / 1000, tz=timezone.utc).date().isoformat(),
    "Open": float(candle[1]),
    "High": float(candle[2]),
    "Low": float(candle[3]),
    "Close": float(candle[4]),
    "Volume": float(candle[5]),
}

df = pd.DataFrame([row])
df.to_csv(OUT_FILE, index=False)

print("✅ OHLCV RAW registado com sucesso")
print(f"📅 Date: {row['Date']}")
print(f"💰 Close: {row['Close']}")
print(f"📁 Ficheiro: {OUT_FILE}")
