from pathlib import Path
import pandas as pd

# =========================================================
# VALIDAÇÃO — BTC DAILY FUSED
# Modo: STREAM VIVO
# Valida integridade, não exige histórico
# =========================================================

print("🛡️ VALIDAÇÃO — BTC DAILY FUSED (STREAM VIVO)")
print("=" * 50)

# ---------------------------------------------------------
# ROOTS
# ---------------------------------------------------------

BASE_PATH = Path(__file__).resolve().parents[2]
DATA_FUSED = BASE_PATH / "data/final/btc_daily_full.csv"

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

if not DATA_FUSED.exists():
    print(f"❌ Ficheiro fused não encontrado: {DATA_FUSED}")
    exit(1)

df = pd.read_csv(DATA_FUSED)

if df.empty:
    print("❌ Ficheiro fused vazio")
    exit(1)

# ---------------------------------------------------------
# BASIC INTEGRITY CHECKS
# ---------------------------------------------------------

required_columns = {"Date", "Open", "High", "Low", "Close"}

missing_cols = required_columns - set(df.columns)
if missing_cols:
    print(f"❌ Colunas em falta: {missing_cols}")
    exit(1)

# ---------------------------------------------------------
# STREAM-AWARE ANALYSIS
# ---------------------------------------------------------

total_days = len(df)
days_without_dominance = df["DominanceBTC"].isna().sum() if "DominanceBTC" in df.columns else total_days

start_date = df["Date"].iloc[0]
end_date   = df["Date"].iloc[-1]

# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

print(f"📊 Registos totais: {total_days}")
print(f"📆 Intervalo: {start_date} → {end_date}")

if "DominanceBTC" not in df.columns:
    print("⚠️ DominanceBTC não existe no dataset")
else:
    print(f"⚠️ Dias sem Dominance: {days_without_dominance}")

# ---------------------------------------------------------
# STREAM MODE DECISION
# ---------------------------------------------------------

print("✅ Validação STREAM OK")
print("🧠 Organismo autorizado a viver com dados parciais.")
print("🫀 Nenhuma correção automática foi aplicada.")
