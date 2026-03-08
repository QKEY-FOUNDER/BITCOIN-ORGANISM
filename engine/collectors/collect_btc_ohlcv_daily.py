import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🩸 PILAR A — OHLCV diário (Binance, candle fechado)")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "ohlcv"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# BINANCE API — BTCUSDT 1d
# =========================================================
url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",
    "interval": "1d",
    "limit": 2
}

resp = requests.get(url, params=params, timeout=30)

if resp.status_code != 200:
    raise RuntimeError("❌ Falha ao obter dados da Binance")

data = resp.json()

if len(data) < 2:
    raise RuntimeError("❌ Dados insuficientes da Binance")

# =========================================================
# Último candle fechado = penúltimo
# =========================================================
closed_candle = data[-2]

open_time = datetime.fromtimestamp(closed_candle[0] / 1000, tz=timezone.utc).date()
today_utc = datetime.now(timezone.utc).date()

if open_time >= today_utc:
    print("⏳ Candle ainda não fechado — ignorado")
    raise SystemExit(0)

row = {
    "Date": open_time.isoformat(),
    "Open": float(closed_candle[1]),
    "High": float(closed_candle[2]),
    "Low": float(closed_candle[3]),
    "Close": float(closed_candle[4]),
    "Volume": float(closed_candle[5]),
}

filename = f"btc_ohlcv_{row['Date']}.csv"
out_file = RAW_DIR / filename

if out_file.exists():
    print(f"⚠️ OHLCV já existe para {row['Date']} — ignorado")
    raise SystemExit(0)

df = pd.DataFrame([row])
df.to_csv(out_file, index=False)

print("✅ OHLCV diário registado com sucesso")
print(f"📅 Date: {row['Date']}")
print(f"📁 Ficheiro: {out_file}")
