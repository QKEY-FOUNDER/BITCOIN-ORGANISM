import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import subprocess
import sys

print("🧠 PIPELINE DIÁRIO — BITCOIN ORGANISM")
print("⏱️ Execução canónica (UTC)")
print("=" * 50)

STEPS = [
    (
        "🩸 Pilar B — Dominance BTC diária",
        ["python3", "engine/collectors/collect_btc_dominance_daily.py"],
    ),
    (
        "🧪 Layer 1 — Normalização Dominance",
        ["python3", "engine/collectors/normalize_btc_dominance_daily.py"],
    ),
    (
        "🩸 Pilar A — OHLCV diário",
        ["python3", "engine/collectors/collect_btc_ohlcv_daily.py"],
    ),
    (
        "🧪 Layer 1 — Normalização OHLCV",
        ["python3", "engine/collectors/normalize_btc_ohlcv_daily.py"],
    ),
    (
        "🧬 Layer 2 — Fusão diária (Market + Dominance)",
        ["python3", "engine/mergers/fuse_daily_market_dominance.py"],
    ),
    (
        "🧾 Validação pós-fusão",
        ["python3", "engine/validators/validate_daily_fused.py"],
    ),
]

for title, command in STEPS:
    print(f"\n▶️ {title}")
    result = subprocess.run(command)

    if result.returncode != 0:
        print("\n❌ PIPELINE INTERROMPIDO")
        sys.exit(result.returncode)

print("\n✅ PIPELINE DIÁRIO CONCLUÍDO COM SUCESSO")
print("🧠 Organismo sincronizado com o tempo.")

# =========================================================
# OBSERVABILIDADE — RESUMO DIÁRIO
# =========================================================
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

fused = DATA_DIR / "fused" / "btc_daily_fused.csv"

if fused.exists():
    df = pd.read_csv(fused, parse_dates=["Date"])
    total = len(df)
    missing_dom = df["DominanceBTC"].isna().sum()
    coverage = 0 if total == 0 else round(100 * (total - missing_dom) / total, 2)

    print("📡 OBSERVABILIDADE")
    print(f"• Registos totais: {total}")
    print(f"• Dias sem Dominance: {missing_dom}")
    print(f"• Cobertura Dominance: {coverage}%")
else:
    print("📡 OBSERVABILIDADE — fused inexistente")
