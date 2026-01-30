from pathlib import Path
import pandas as pd
from datetime import datetime

# ============================================================
# GEO NORMALIZER — robust root detection (CANÓNICO)
# ============================================================

def find_project_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / "data_geo").exists():
            return parent
    raise RuntimeError("Project root with data_geo/ not found")

BASE_PATH = find_project_root(Path(__file__).resolve())

RAW_EXCHANGE = BASE_PATH / "data_geo/monthly_exchange_dominance"
RAW_REGION   = BASE_PATH / "data_geo/monthly_region_dominance"

OUT_EXCHANGE = BASE_PATH / "data_geo/normalized/monthly_exchange_dominance"
OUT_REGION   = BASE_PATH / "data_geo/normalized/monthly_region_dominance"

REPORTS_DIR  = BASE_PATH / "data_geo/reports"
LOG_FILE     = REPORTS_DIR / "geo_normalization.log"

OUT_EXCHANGE.mkdir(parents=True, exist_ok=True)
OUT_REGION.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def log(message: str):
    ts = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {message}\n")

def normalize_file(csv_path: Path, out_dir: Path, expected_cols: list):
    try:
        df = pd.read_csv(csv_path)

        if list(df.columns) != expected_cols:
            log(f"SKIP {csv_path.name} | estrutura inválida {list(df.columns)}")
            return

        df = df.dropna()
        df[expected_cols[0]] = (
            df[expected_cols[0]]
            .astype(str)
            .str.strip()
            .str.lower()
        )
        df[expected_cols[1]] = pd.to_numeric(df[expected_cols[1]], errors="coerce")
        df = df.dropna()

        total = df[expected_cols[1]].sum()
        if not 0.99 <= total <= 1.01:
            log(f"SKIP {csv_path.name} | soma dominance inválida ({total})")
            return

        out_path = out_dir / csv_path.name
        df.to_csv(out_path, index=False)
        log(f"OK {csv_path.name} -> normalized")

    except Exception as e:
        log(f"ERROR {csv_path.name} | {e}")

def run():
    log("=== GEO NORMALIZATION START ===")

    exchange_files = list(RAW_EXCHANGE.glob("*.csv"))
    region_files   = list(RAW_REGION.glob("*.csv"))

    log(f"Encontrados exchange: {len(exchange_files)} | region: {len(region_files)}")

    for f in exchange_files:
        normalize_file(
            csv_path=f,
            out_dir=OUT_EXCHANGE,
            expected_cols=["exchange", "dominance"]
        )

    for f in region_files:
        normalize_file(
            csv_path=f,
            out_dir=OUT_REGION,
            expected_cols=["region", "dominance"]
        )

    log("=== GEO NORMALIZATION END ===")

if __name__ == "__main__":
    run()
