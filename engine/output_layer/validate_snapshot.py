import json
from pathlib import Path
import sys

print("VALIDACAO — ORGANISM SNAPSHOT")
print("=" * 50)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = PROJECT_ROOT / "data" / "organism_snapshot.json"

if not SNAPSHOT_PATH.exists():
    print(f"Snapshot nao encontrado: {SNAPSHOT_PATH}")
    sys.exit(1)

with open(SNAPSHOT_PATH) as f:
    snapshot = json.load(f)

required_top_fields = {
    "date",
    "regime",
    "allocation",
    "risk_state",
    "btc_price"
}

missing = required_top_fields - snapshot.keys()

if missing:
    print(f"Campos obrigatorios em falta: {missing}")
    sys.exit(1)

if not isinstance(snapshot["date"], str):
    print("Campo 'date' deve ser string")
    sys.exit(1)

if not isinstance(snapshot["regime"], str):
    print("Campo 'regime' deve ser string")
    sys.exit(1)

if not isinstance(snapshot["btc_price"], (int, float)):
    print("Campo 'btc_price' deve ser numerico")
    sys.exit(1)

allocation = snapshot["allocation"]
if not isinstance(allocation, dict):
    print("Campo 'allocation' deve ser dict")
    sys.exit(1)

btc_w = allocation.get("BTC_Weight")
cash_w = allocation.get("Cash_Weight")

if btc_w is None or cash_w is None:
    print("Allocation incompleta")
    sys.exit(1)

if not (0 <= btc_w <= 1 and 0 <= cash_w <= 1):
    print("Pesos fora do intervalo 0-1")
    sys.exit(1)

if round(btc_w + cash_w, 4) != 1.0:
    print("Pesos nao somam 1.0")
    sys.exit(1)

risk_state = snapshot["risk_state"]
if not isinstance(risk_state, dict):
    print("Campo 'risk_state' deve ser dict")
    sys.exit(1)

required_risk_fields = {"risk_score", "stress_trend", "volatility_score"}

missing_risk = required_risk_fields - risk_state.keys()

if missing_risk:
    print(f"Campos risk_state em falta: {missing_risk}")
    sys.exit(1)

print("Snapshot estruturalmente valido.")
