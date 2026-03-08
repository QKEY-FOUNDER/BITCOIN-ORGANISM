from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

from pathlib import Path
import pandas as pd
import sys

# =========================================================
# GEO ENGINE — Órgão Sensorial Passivo
# Read-only | Memória mensal lenta
# =========================================================

print("🌍 GEO ENGINE — BTC DAILY (READ-ONLY)")
print("=" * 50)

# ---------------------------------------------------------
# ROOTS
# ---------------------------------------------------------

ENGINE_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH   = ENGINE_ROOT.parents[2]

DATA_GEO = BASE_PATH / "data_geo"

REGION_DOM_DIR   = DATA_GEO / "monthly_region_dominance"
EXCHANGE_DOM_DIR = DATA_GEO / "monthly_exchange_dominance"

# ---------------------------------------------------------
# ARGUMENTS
# ---------------------------------------------------------

target_month = sys.argv[1] if len(sys.argv) > 1 else None

print(f"🗓️  Mês alvo: {target_month if target_month else 'auto'}")

# ---------------------------------------------------------
# RESOLVE MONTH (PASSIVE)
# ---------------------------------------------------------

def resolve_month():
    if target_month:
        return target_month

    # modo diário → usa mês atual mas NÃO reage
    from datetime import datetime
    return datetime.utcnow().strftime("%Y_%m")

month = resolve_month()

# ---------------------------------------------------------
# LOAD PASSIVE GEO MEMORY
# ---------------------------------------------------------

region_file   = REGION_DOM_DIR / f"{month}.csv"
exchange_file = EXCHANGE_DOM_DIR / f"{month}.csv"

geo_memory = {
    "month": month,
    "regions_available": False,
    "exchanges_available": False,
    "confidence": "low"
}

if region_file.exists():
    geo_memory["regions_available"] = True

if exchange_file.exists():
    geo_memory["exchanges_available"] = True

# ---------------------------------------------------------
# OUTPUT (PASSIVE ONLY)
# ---------------------------------------------------------

if geo_memory["regions_available"] or geo_memory["exchanges_available"]:
    print("🧠 GEO MEMÓRIA PASSIVA DETETADA")
    print(f"• Região:   {geo_memory['regions_available']}")
    print(f"• Exchanges: {geo_memory['exchanges_available']}")
    print("• Confiança: baixa")
else:
    print("⚠️ Nenhuma memória GEO disponível")

print("\n🌐 GEO VECTOR (passivo):")
for k, v in geo_memory.items():
    print(f"  • {k}: {v}")

print("\n🧠 GEO Engine ativo em modo observação.")
