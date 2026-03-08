from pathlib import Path
from engine.memory_engine.regime_memory import RegimeMemory

# engine/state_engine/state_engine.py
# ============================================================
# STATE ENGINE — Sistema Nervoso Central
# Read-only | Observação canónica
# ============================================================

# ================================
# HARDENING (sempre primeiro)
# ================================
from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

# ================================
# IMPORTS
# ================================
from pathlib import Path
import pandas as pd

from engine.immune_system.immune_engine import immune_response
from engine.observability.health_engine import get_health_state
from engine.output_layer.output_engine import render_output

# ================================
# BANNER
# ================================
print("🧠 STATE ENGINE — BTC DAILY (READ-ONLY)")
print("Modo: observação canónica")
print("=" * 60)

# ================================
# ROOTS
# ================================
BASE_PATH = Path(__file__).resolve().parents[2]
DATA_FINAL = BASE_PATH / "data/final"
DATA_FUSED = DATA_FINAL / "btc_daily_full.csv"

# ================================
# LOAD DATA (read-only)
# ================================
if not DATA_FUSED.exists():
    raise FileNotFoundError(f"Ficheiro fused não encontrado: {DATA_FUSED}")

df = pd.read_csv(DATA_FUSED)
last_row = df.iloc[-1]

date = last_row["Date"]
close = last_row["Close"]
dominance = last_row.get("Dominance", None)

print(f"📅 Data: {date}")
print(f"💰 Close: {close}")

# ================================
# CANONICAL STATE RESOLUTION
# ================================

# Preço (simplificado nesta fase)
price_state = "transition"

# Dominance / Macro
if pd.isna(dominance):
    macro_state = "no_dominance"
    interpretation = "macro_blind"
else:
    macro_state = "dominant"
    interpretation = "macro_visible"

# GEO (canónico por agora)
geo_state = "geo_silent"

canonical_state = {
    "date": date,
    "price_state": price_state,
    "macro_state": macro_state,
    "geo_state": geo_state,
    "interpretation": interpretation,
}

print("\n🧬 Estado canónico composto:")
print(f"• Preço: {price_state}")
print(f"• Macro (Dominance): {macro_state}")
print(f"• GEO: {geo_state}")
print(f"• Interpretação: {interpretation}")

from engine.state_engine.regime_memory import update_regime_memory

regime_memory = update_regime_memory(canonical_state)
# ============================================================
# 🧠 REGIME CONFIRMATION LAYER
# Confirma se o regime já é persistente
# ============================================================

from engine.memory_engine.regime_memory import RegimeMemory

memory = RegimeMemory(
    snapshot_dir=Path("data/07_global_reckoning_2022_infinity/snapshots/daily"),
    min_days=3
)

regime_info = memory.current_regime()

if regime_info:
    canonical_state["regime_confirmed"] = True
    canonical_state["regime_duration"] = regime_info.get("duration_days", 0)
else:
    canonical_state["regime_confirmed"] = False
    canonical_state["regime_duration"] = 0

# ================================
# HEALTH ENGINE
# ================================
health_state = get_health_state()

print("\n❤️ Saúde do Organismo:")
print(f"• health_state: {health_state}")

# ================================
# IMMUNE SYSTEM
# ================================
immune = immune_response(
    price_state=canonical_state["price_state"],
    macro_state=canonical_state["macro_state"],
    geo_state=canonical_state["geo_state"],
    health_state=health_state,
)

print("\n🛡️ Resposta Imunitária:")
for k, v in immune.items():
    print(f"• {k}: {v}")

# ============================================================
# OUTPUT LAYER — EXPRESSÃO FINAL
# ============================================================

from engine.output_layer.snapshot_writer import write_daily_snapshot
from engine.output_layer.output_engine import render_output

output = render_output(
    canonical_state=canonical_state,
    health_state=health_state,
    immune=immune,
)

from engine.output_layer.snapshot_writer import write_daily_snapshot

snapshot_file = write_daily_snapshot(
    canonical_state=canonical_state,
    health_state=health_state,
    immune=immune,
    output=output,
)

print(f"🫀 Batimento diário selado em: {snapshot_file}")

from engine.output_layer.symbolic_signature import sign_snapshot

signature_file = sign_snapshot(snapshot_file)

print(f"🔐 Assinatura simbólica criada em: {signature_file}")

from engine.output_layer.snapshot_integrity import verify_snapshot_integrity
from pathlib import Path

snapshot_path = Path(snapshot_file)
hash_path = snapshot_path.with_suffix(".hash")

integrity = verify_snapshot_integrity(snapshot_path, hash_path)

print("🔎 Integridade do Snapshot:")
for k, v in integrity.items():
    print(f" - {k}: {v}")
from engine.output_layer.heartbeat_writer import write_heartbeat

heartbeat_file = write_heartbeat(
    date=canonical_state["date"],
    health_state=health_state,
    immune_action=immune["action"],
    snapshot_file=snapshot_file,
)

print(f"🕯️ Heartbeat diário registado em: {heartbeat_file}")
