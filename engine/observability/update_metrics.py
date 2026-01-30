import json
import pandas as pd
from pathlib import Path

print("📡 OBSERVABILIDADE — UPDATE MÉTRICAS")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
METRICS_DIR = DATA_DIR / "metrics"
FUSED_FILE = DATA_DIR / "fused" / "btc_daily_fused.csv"
METRICS_FILE = METRICS_DIR / "observability.json"

# =========================================================
# GARANTIR DIRETÓRIO
# =========================================================
METRICS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# MÉTRICAS BASE
# =========================================================
metrics = {
    "total_days": 0,
    "days_without_dominance": 0,
    "dominance_coverage_pct": 0.0,
}

# =========================================================
# LOAD FUSED
# =========================================================
if not FUSED_FILE.exists():
    print(f"❌ Ficheiro fused não encontrado: {FUSED_FILE}")
else:
    df = pd.read_csv(FUSED_FILE, parse_dates=["Date"])

    metrics["total_days"] = int(len(df))
    metrics["days_without_dominance"] = int(df["DominanceBTC"].isna().sum())

    if metrics["total_days"] > 0:
        metrics["dominance_coverage_pct"] = round(
            100
            * (metrics["total_days"] - metrics["days_without_dominance"])
            / metrics["total_days"],
            2,
        )

# =========================================================
# WRITE METRICS
# =========================================================
METRICS_FILE.write_text(json.dumps(metrics, indent=2))

# =========================================================
# STDOUT COMPACTO (CANÓNICO)
# =========================================================
print("✅ Observabilidade atualizada")
print(f"📊 Dias totais: {metrics['total_days']}")
print(f"⚠️ Dias sem Dominance: {metrics['days_without_dominance']}")
print(f"📈 Cobertura Dominance: {metrics['dominance_coverage_pct']}%")
