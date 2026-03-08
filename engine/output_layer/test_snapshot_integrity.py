from pathlib import Path
import json
from datetime import datetime

print("🧪 TESTE DE INTEGRIDADE — ORGANISM SNAPSHOT")
print("=" * 50)


def main():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    SNAPSHOT_FILE = PROJECT_ROOT / "data" / "organism_snapshot.json"

    if not SNAPSHOT_FILE.exists():
        raise RuntimeError("Snapshot não encontrado")

    with open(SNAPSHOT_FILE, "r") as f:
        snapshot = json.load(f)

    errors = []

    # -------------------------
    # Estrutura base
    # -------------------------
    required_top = ["date", "regime", "btc_price", "allocation", "risk_state"]

    for field in required_top:
        if field not in snapshot:
            errors.append(f"Campo em falta: {field}")

    if errors:
        print("❌ Erros estruturais detectados:")
        for e in errors:
            print("-", e)
        return

    allocation = snapshot["allocation"]
    risk_state = snapshot["risk_state"]

    # -------------------------
    # Validação de data
    # -------------------------
    try:
        datetime.strptime(snapshot["date"], "%Y-%m-%d")
    except:
        errors.append("Formato de data inválido (esperado YYYY-MM-DD)")

    # -------------------------
    # Validação de pesos
    # -------------------------
    btc_weight = allocation.get("BTC_Weight", None)
    cash_weight = allocation.get("Cash_Weight", None)

    if btc_weight is None or cash_weight is None:
        errors.append("Pesos de alocação incompletos")
    else:
        total = round(btc_weight + cash_weight, 5)
        if total != 1.0:
            errors.append(f"Soma dos pesos != 1 (atual: {total})")

    # -------------------------
    # Validação de risco
    # -------------------------
    risk_score = risk_state.get("risk_score", None)
    volatility_score = risk_state.get("volatility_score", None)

    if risk_score is None or not (0 <= risk_score <= 1):
        errors.append("risk_score fora do intervalo [0,1]")

    if volatility_score is None or not (0 <= volatility_score <= 1):
        errors.append("volatility_score fora do intervalo [0,1]")

    # -------------------------
    # Regime válido
    # -------------------------
    valid_regimes = {"calm", "volatile", "crisis"}

    if snapshot["regime"] not in valid_regimes:
        errors.append(f"Regime inválido: {snapshot['regime']}")

    # -------------------------
    # Resultado
    # -------------------------
    if errors:
        print("❌ Falhas de integridade detectadas:")
        for e in errors:
            print("-", e)
    else:
        print("✅ Snapshot semanticamente íntegro.")
        print("🧬 ADN consistente.")
        print("=" * 50)


if __name__ == "__main__":
    main()
