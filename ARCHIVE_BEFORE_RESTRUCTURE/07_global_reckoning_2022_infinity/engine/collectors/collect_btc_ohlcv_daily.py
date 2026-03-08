import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🩸 PILAR A — OHLCV diário (job canónico)")

# =========================================================
# PROJECT ROOT (inequívoco)
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "ohlcv"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# DATA DO DIA (UTC)
# =========================================================
today_utc = datetime.now(timezone.utc).date()
filename = f"btc_ohlcv_{today_utc}.csv"
out_file = RAW_DIR / filename

if out_file.exists():
    print(f"⚠️ OHLCV já existe para {today_utc} — ignorado")
    raise SystemExit(0)

# =========================================================
# COLETA (PLACEHOLDER ESTRUTURAL)
# =========================================================
data = {
    "Date": [today_utc.isoformat()],
    "Open": [None],
    "High": [None],
    "Low": [None],
    "Close": [None],
    "Volume": [None],
}

df = pd.DataFrame(data)

# =========================================================
# WRITE RAW
# =========================================================
df.to_csv(out_file, index=False)

print("✅ OHLCV diário registado com sucesso")
print(f"📁 Ficheiro: {out_file}")
