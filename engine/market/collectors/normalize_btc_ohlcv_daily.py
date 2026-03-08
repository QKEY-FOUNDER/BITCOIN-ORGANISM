import pandas as pd
from pathlib import Path

print("🧪 BATIMENTO 2 — Normalização OHLCV diária")

# =========================================================
# PROJECT ROOT (RAIZ REAL)
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# =========================================================
# PATHS CANÓNICOS
# =========================================================
DATA_DIR = PROJECT_ROOT / "data" / "market"

RAW_DIR = DATA_DIR / "raw" / "ohlcv"
OUT_DIR = DATA_DIR / "normalized"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = OUT_DIR / "btc_ohlcv_daily.csv"

# =========================================================
# LOAD RAW FILES
# =========================================================
files = sorted(RAW_DIR.glob("btc_ohlcv_*_raw.csv"))

if not files:
    raise RuntimeError(f"❌ Nenhum ficheiro encontrado em {RAW_DIR}")

frames = []

for f in files:
    df = pd.read_csv(f)
    df.columns = [c.strip() for c in df.columns]

    required_cols = {"Date", "Open", "High", "Low", "Close", "Volume"}
    if not required_cols.issubset(df.columns):
        raise RuntimeError(f"❌ Colunas inválidas em {f.name}")

    frames.append(df[list(required_cols)])

# =========================================================
# CONCAT + CLEAN
# =========================================================
merged = (
    pd.concat(frames, ignore_index=True)
      .drop_duplicates(subset=["Date"])
      .sort_values("Date")
)

merged.to_csv(OUT_FILE, index=False)

print("✅ OHLCV diário normalizado criado com sucesso")
print(f"📁 Ficheiro: {OUT_FILE}")
print(f"📊 Registos: {len(merged)}")
print(f"📆 Intervalo: {merged['Date'].min()} → {merged['Date'].max()}")
