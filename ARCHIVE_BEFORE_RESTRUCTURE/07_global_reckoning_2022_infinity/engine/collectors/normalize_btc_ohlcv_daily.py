import pandas as pd
from pathlib import Path

print("🧠 BATIMENTO 2 — Normalização OHLCV diária")

# =========================================================
# PROJECT ROOT (07_global_reckoning_2022_infinity)
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =========================================================
# PATHS REAIS (CONFIRMADOS NO DISCO)
# =========================================================
RAW_DIR = PROJECT_ROOT / "raw" / "ohlcv"
OUT_DIR = PROJECT_ROOT / "data" / "normalized"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = OUT_DIR / "btc_ohlcv_daily.csv"

# =========================================================
# LOAD RAW FILES
# =========================================================
files = sorted(RAW_DIR.glob("btc_ohlcv_*.csv"))

if not files:
    raise RuntimeError(f"❌ Nenhum ficheiro encontrado em {RAW_DIR}")

frames = []

for f in files:
    df = pd.read_csv(f)
    df.columns = [c.strip() for c in df.columns]

    if "Date" not in df.columns:
        raise RuntimeError(f"❌ Ficheiro sem coluna Date: {f.name}")

    df["Date"] = pd.to_datetime(df["Date"])
    frames.append(df)

# =========================================================
# MERGE + CLEAN
# =========================================================
merged = (
    pd.concat(frames, ignore_index=True)
      .drop_duplicates(subset=["Date"])
      .sort_values("Date")
)

merged.to_csv(OUT_FILE, index=False)

print("🟢 OHLCV diário normalizado criado com sucesso")
print(f"📁 {OUT_FILE}")
print(f"📊 Registos: {len(merged)}")
print(f"📆 Intervalo: {merged['Date'].min().date()} → {merged['Date'].max().date()}")
