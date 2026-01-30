import pandas as pd
from pathlib import Path
import sys

print("🛡️ VALIDAÇÃO — DOMINANCE BTC DIÁRIA")
print("=" * 50)

# =========================================================
# ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DOM_FILE = DATA_DIR / "normalized" / "dominance_daily.csv"

# =========================================================
# GUARDA ABSOLUTA
# =========================================================

if not DOM_FILE.exists():
    print(f"❌ Ficheiro não encontrado: {DOM_FILE}")
    sys.exit(1)

# =========================================================
# LOAD
# =========================================================

df = pd.read_csv(DOM_FILE, parse_dates=["Date"])

# =========================================================
# ESTRUTURA
# =========================================================

expected_cols = ["Date", "DominanceBTC"]
if list(df.columns) != expected_cols:
    print("❌ Estrutura inválida")
    print("Esperado:", expected_cols)
    print("Encontrado:", list(df.columns))
    sys.exit(1)

# =========================================================
# TEMPO
# =========================================================

if df["Date"].isna().any():
    print("❌ Datas inválidas (NaT)")
    sys.exit(1)

if not df["Date"].is_monotonic_increasing:
    print("❌ Datas não estão ordenadas")
    sys.exit(1)

if df["Date"].duplicated().any():
    dups = df["Date"].duplicated().sum()
    print(f"❌ Datas duplicadas encontradas: {dups}")
    sys.exit(1)

# =========================================================
# DOMINANCE RANGE
# =========================================================

dom = df["DominanceBTC"]

if dom.isna().any():
    missing = dom.isna().sum()
    print(f"⚠️ Aviso: {missing} dias sem Dominance")

if ((dom < 0) | (dom > 100)).any():
    print("❌ Valores de Dominance fora do intervalo [0,100]")
    sys.exit(1)

# =========================================================
# OK
# =========================================================

print("✅ Validação Dominance BTC OK")
print(f"📊 Registos: {len(df)}")
print(f"📆 Intervalo: {df['Date'].min().date()} → {df['Date'].max().date()}")
