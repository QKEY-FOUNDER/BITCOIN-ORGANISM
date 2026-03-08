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

from engine.state_engine.snapshot_seal import seal_snapshot
from engine.state_engine.regime_memory import update_regime_memory
from engine.immune_system.immune_engine import immune_response
from engine.observability.health_engine import get_health_state
from engine.output_layer.output_engine import render_output

from engine.output_layer.snapshot_writer import write_daily_snapshot
from engine.output_layer.symbolic_signature import sign_snapshot
from engine.output_layer.snapshot_integrity import verify_snapshot_integrity
from engine.output_layer.heartbeat_writer import write_heartbeat

# ================================
# BANNER
# ================================
print("🧠 STATE ENGINE — BTC DAILY (READ-ONLY)")
print("Modo: observação canónica")
print("=" * 60)


# =========================================================
# ROOTS
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FUSED = PROJECT_ROOT / "data" / "final" / "btc_daily_full.csv"

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
price_state = "transition"

if pd.isna(dominance):
    macro_state = "no_dominance"
    interpretation = "macro_blind"
else:
    macro_state = "dominant"
    interpretation = "macro_visible"

geo_state = "geo_silent"

canonical_state = {
    "date": date,
    "price_state": price_state,
    "macro_state": macro_state,
    "geo_state": geo_state,
    "interpretation": interpretation,
}

print("\n🧬 Estado canónico composto:")
for k, v in canonical_state.items():
    print(f"• {k}: {v}")

# ============================================================
# 1️⃣ SNAPSHOT SEAL (MEMÓRIA PRIMÁRIA)
# ============================================================
seal_snapshot(canonical_state)

# ============================================================
# 2️⃣ REGIME MEMORY (AGORA COM PASSADO REAL)
# ============================================================
regime_memory = update_regime_memory(canonical_state)

# Extrair estabilidade harmónica
regime_data = regime_memory.get("regime", {})

canonical_state["regime"] = regime_data.get("value", "unknown")
canonical_state["regime_duration"] = regime_data.get("days", 0)
canonical_state["stability_ratio"] = regime_data.get("stability_ratio", 0.0)
canonical_state["regime_confirmed"] = canonical_state["stability_ratio"] >= 0.6

print("\n🧠 Regimes persistentes:")
for k, v in regime_memory.items():
    print(f"• {k}: {v['value']} ({v['days']} dias)")

# ============================================================
# 3️⃣ HEALTH ENGINE
# ============================================================
health_state = get_health_state()

print("\n❤️ Saúde do Organismo:")
print(f"• health_state: {health_state}")

# ============================================================
# 4️⃣ IMMUNE SYSTEM
# ============================================================
immune = immune_response(
    price_state=canonical_state["price_state"],
    macro_state=canonical_state["macro_state"],
    geo_state=canonical_state["geo_state"],
    health_state=health_state["health_state"],
    stability_ratio=canonical_state.get("stability_ratio", 0.0),
)

print("\n🛡️ Resposta Imunitária:")
for k, v in immune.items():
    print(f"• {k}: {v}")

# ============================================================
# 5️⃣ OUTPUT LAYER
# ============================================================
output = render_output(
    canonical_state=canonical_state,
    health_state=health_state,
    immune=immune,
)

# ============================================================
# 6️⃣ SNAPSHOT FINAL + INTEGRIDADE
# ============================================================
snapshot_file = write_daily_snapshot(
    canonical_state=canonical_state,
    health_state=health_state,
    immune=immune,
    output=output,
)

print(f"\n🫀 Batimento diário selado em: {snapshot_file}")

signature_file = sign_snapshot(snapshot_file)
print(f"🔐 Assinatura simbólica criada em: {signature_file}")

snapshot_path = Path(snapshot_file)
hash_path = snapshot_path.with_suffix(".hash")

integrity = verify_snapshot_integrity(snapshot_path, hash_path)

print("\n🔎 Integridade do Snapshot:")
for k, v in integrity.items():
    print(f" - {k}: {v}")

# ============================================================
# 7️⃣ HEARTBEAT
# ============================================================
heartbeat_file = write_heartbeat(
    date=canonical_state["date"],
    health_state=health_state,
    immune_action=immune["action"],
    snapshot_file=snapshot_file,
)

print(f"\n🕯️ Heartbeat diário registado em: {heartbeat_file}")
