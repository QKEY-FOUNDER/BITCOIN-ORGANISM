from pathlib import Path

# =========================================================
# PROJECT ROOT (VERDADE ÚNICA)
# =========================================================
# paths.py vive em:
# data/07_global_reckoning_2022_infinity/config/paths.py
#
# parents[1] = 07_global_reckoning_2022_infinity
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# =========================================================
# DATA ROOT
# =========================================================
DATA_ROOT = PROJECT_ROOT / "data"

# =========================================================
# RAW DATA
# =========================================================
RAW_ROOT = DATA_ROOT / "raw"

RAW_OHLCV_DAILY = RAW_ROOT / "ohlcv"
RAW_DOMINANCE_DAILY = RAW_ROOT / "dominance"

# =========================================================
# NORMALIZED DATA
# =========================================================
NORMALIZED_ROOT = DATA_ROOT / "normalized"

NORMALIZED_OHLCV_DAILY = NORMALIZED_ROOT / "btc_ohlcv_daily.csv"
NORMALIZED_DOMINANCE_DAILY = NORMALIZED_ROOT / "dominance_daily.csv"

# =========================================================
# FINAL DATASETS
# =========================================================
FINAL_ROOT = DATA_ROOT / "final"

FINAL_DAILY_DATASET = FINAL_ROOT / "btc_daily_FULL.csv"

# =========================================================
# ENSURE DIRECTORIES EXIST
# =========================================================
for d in [
    RAW_OHLCV_DAILY,
    RAW_DOMINANCE_DAILY,
    NORMALIZED_ROOT,
    FINAL_ROOT,
]:
    d.mkdir(parents=True, exist_ok=True)
