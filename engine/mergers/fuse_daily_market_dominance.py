import pandas as pd
from pathlib import Path

print("🧬 LAYER 2 — FUSÃO DIÁRIA (Market + Dominance)")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
NORMALIZED_DIR = DATA_DIR / "normalized"
FINAL_DIR = DATA_DIR / "final"

FINAL_DIR.mkdir(parents=True, exist_ok=True)

OHLCV_FILE = NORMALIZED_DIR / "btc_ohlcv_daily.csv"
DOM_FILE   = NORMALIZED_DIR / "dominance_daily.csv"
OUT_FILE   = FINAL_DIR / "btc_daily_full.csv"

# =========================================================
# GUARDAS CRÍTICAS
# =========================================================
if not OHLCV_FILE.exists():
    raise RuntimeError(f"❌ OHLCV diário normalizado não encontrado: {OHLCV_FILE}")

if not DOM_FILE.exists():
    raise RuntimeError(f"❌ Dominance normalizada não encontrada: {DOM_FILE}")

# =========================================================
# LOAD DATA
# =========================================================
ohlcv = pd.read_csv(OHLCV_FILE, parse_dates=["Date"])
dom   = pd.read_csv(DOM_FILE, parse_dates=["Date"])

ohlcv.columns = [c.strip() for c in ohlcv.columns]
dom.columns   = [c.strip() for c in dom.columns]

if "DominanceBTC" not in dom.columns:
    raise RuntimeError("❌ Coluna 'DominanceBTC' não encontrada")

# =========================================================
# FUSÃO — OHLCV É O EIXO PRINCIPAL
# =========================================================
fused = (
    ohlcv
    .merge(dom[["Date", "DominanceBTC"]], on="Date", how="left")
    .sort_values("Date")
)

# Garantir que não existem dias sem preço
fused = fused.dropna(subset=["Close"])

# =========================================================
# VALIDAÇÃO
# =========================================================
missing_dom = fused["DominanceBTC"].isna().sum()

if missing_dom > 0:
    print(f"⚠️ {missing_dom} dias sem Dominance (mantidos como NaN)")

# =========================================================
# OUTPUT
# =========================================================
fused.to_csv(OUT_FILE, index=False)

print("✅ BTC DAILY FUSED CRIADO COM SUCESSO")
print(f"📁 Ficheiro: {OUT_FILE}")
print(f"📊 Registos: {len(fused)}")
print(f"📆 Intervalo: {fused['Date'].min().date()} → {fused['Date'].max().date()}")
