from pathlib import Path
import pandas as pd
from datetime import datetime

# ============================================================
# GEO MONTHLY VALIDATOR — read-only sanity check
# ============================================================

def find_project_root(start: Path) -> Path:
    for parent in start.parents:
        if (parent / "data_geo").exists():
            return parent
    raise RuntimeError("Project root with data_geo/ not found")

BASE_PATH = find_project_root(Path(__file__).resolve())

NORM_EXCHANGE = BASE_PATH / "data_geo/normalized/monthly_exchange_dominance"
NORM_REGION   = BASE_PATH / "data_geo/normalized/monthly_region_dominance"

REPORTS_DIR = BASE_PATH / "data_geo/reports"
LOG_FILE = REPORTS_DIR / "geo_monthly_validator.log"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def log(message: str):
    ts = datetime.utcnow().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {message}\n")

def validate_folder(folder: Path, expected_cols: list, label: str):
    ok = 0
    errors = 0
    months = []

    for csv in sorted(folder.glob("*.csv")):
        month = csv.stem
        months.append(month)

        try:
            df = pd.read_csv(csv)

            if list(df.columns) != expected_cols:
                log(f"ERROR {label} {month} | colunas inválidas {list(df.columns)}")
                errors += 1
                continue

            if df.isna().any().any():
                log(f"ERROR {label} {month} | NaN detectado")
                errors += 1
                continue

            total = df[expected_cols[1]].sum()
            if not 0.99 <= total <= 1.01:
                log(f"ERROR {label} {month} | soma dominance inválida ({total})")
                errors += 1
                continue

            ok += 1

        except Exception as e:
            log(f"ERROR {label} {month} | {e}")
            errors += 1

    # verificar continuidade temporal
    if months:
        sorted_months = sorted(months)
        gaps = []
        for i in range(1, len(sorted_months)):
            y1, m1 = map(int, sorted_months[i-1].split("_"))
            y2, m2 = map(int, sorted_months[i].split("_"))
            if (y2 * 12 + m2) - (y1 * 12 + m1) != 1:
                gaps.append((sorted_months[i-1], sorted_months[i]))

        if gaps:
            log(f"WARN {label} gaps temporais: {gaps}")

    return ok, errors

def run():
    log("=== GEO MONTHLY VALIDATION START ===")

    ex_ok, ex_err = validate_folder(
        NORM_EXCHANGE,
        ["exchange", "dominance"],
        "exchange"
    )

    reg_ok, reg_err = validate_folder(
        NORM_REGION,
        ["region", "dominance"],
        "region"
    )

    log(
        f"SUMMARY exchange_ok={ex_ok} exchange_err={ex_err} | "
        f"region_ok={reg_ok} region_err={reg_err}"
    )

    log("=== GEO MONTHLY VALIDATION END ===")

if __name__ == "__main__":
    run()
