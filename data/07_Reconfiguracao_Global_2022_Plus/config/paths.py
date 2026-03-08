from pathlib import Path

# =========================================================
# ROOT
# =========================================================
ROOT = Path(__file__).resolve().parents[1]

# =========================================================
# DATA DIRECTORIES
# =========================================================
DATA_DIR = ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
NORMALIZED_DIR = DATA_DIR / "normalized"
FINAL_DIR = DATA_DIR / "final"

RAW_OHLCV_DIR = RAW_DIR / "ohlcv"

# =========================================================
# FILES — NORMALIZED
# =========================================================
NORMALIZED_OHLCV_DAILY = NORMALIZED_DIR / "btc_ohlcv_daily.csv"
NORMALIZED_DOMINANCE_DAILY = NORMALIZED_DIR / "dominance_daily.csv"

# =========================================================
# FILES — FINAL
# =========================================================
FINAL_DAILY_DATASET = FINAL_DIR / "btc_daily_FULL.csv"
