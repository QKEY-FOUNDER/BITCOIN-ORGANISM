from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

from pathlib import Path
import pandas as pd

# ===============================================
# HEALTH ENGINE — ORGANISM LONG-RUN (READ-ONLY)
# ===============================================

BASE_PATH = Path(__file__).resolve().parents[2]
DATA_FINAL = BASE_PATH / "data/final/btc_daily_full.csv"


def get_health_state():
    """
    Avalia a saúde de longo prazo do organismo.
    Retorna um dict canónico consumido pelo Immune / State Engine.
    """

    if not DATA_FINAL.exists():
        return {
            "health_state": "fragile",
            "reason": "no_fused_data",
            "metrics": {}
        }

    df = pd.read_csv(DATA_FINAL)

    if df.empty:
        return {
            "health_state": "fragile",
            "reason": "empty_fused_data",
            "metrics": {}
        }

    total_days = len(df)
    days_with_dom = df["DominanceBTC"].notna().sum()

    gaps = df["DominanceBTC"].isna().astype(int)
    max_gap = gaps.groupby((gaps != gaps.shift()).cumsum()).sum().max()

    coverage = round((days_with_dom / total_days) * 100, 2)

    if coverage < 90 or max_gap >= 3:
        health = "fragile"
    else:
        health = "healthy"

    return {
        "health_state": health,
        "reason": "long_run_evaluation",
        "metrics": {
            "days_total": total_days,
            "days_with_dominance": days_with_dom,
            "coverage_pct": coverage,
            "max_gap_days": int(max_gap) if pd.notna(max_gap) else 0
        }
    }


# Execução direta (debug local)
if __name__ == "__main__":
    print("🧬 HEALTH ENGINE — ORGANISM LONG-RUN")
    state = get_health_state()
    for k, v in state.items():
        print(f"{k}: {v}")
