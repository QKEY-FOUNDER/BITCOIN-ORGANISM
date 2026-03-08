from pathlib import Path
import json

print("🎼 RENDER FROM EVOLVED SNAPSHOT")


def main():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    SNAPSHOT_FILE = PROJECT_ROOT / "data" / "organism_snapshot_evolved.json"

    if not SNAPSHOT_FILE.exists():
        raise RuntimeError("Snapshot evoluído não encontrado")

    with open(SNAPSHOT_FILE, "r") as f:
        snapshot = json.load(f)

    required_top = ["date", "regime", "btc_price", "allocation", "risk_state"]

    missing = [k for k in required_top if k not in snapshot]
    if missing:
        raise RuntimeError(f"Campos em falta no snapshot: {missing}")

    allocation = snapshot["allocation"]
    risk_state = snapshot["risk_state"]

    regime = snapshot["regime"]
    btc_price = snapshot["btc_price"]

    btc_weight = allocation["BTC_Weight"]
    cash_weight = allocation["Cash_Weight"]

    risk_score = risk_state["risk_score"]
    stress_trend = risk_state["stress_trend"]
    volatility_score = risk_state["volatility_score"]
    mutation_bias = risk_state.get("mutation_bias", "neutral")

    if regime == "calm":
        mood = "MAJOR"
    elif regime == "volatile":
        mood = "MINOR"
    else:
        mood = "DISSONANT"

    intensity = round(risk_score * 100)

    print("\n🧬 SNAPSHOT EVOLUÍDO LIDO COM SUCESSO")
    print(f"Data: {snapshot['date']}")
    print(f"Regime: {regime}")
    print(f"Preço BTC: {btc_price}")
    print(f"Alocação BTC: {btc_weight}")
    print(f"Alocação Cash: {cash_weight}")
    print(f"Stress Trend: {stress_trend}")
    print(f"Volatilidade: {volatility_score}")
    print(f"Mutation Bias: {mutation_bias}")
    print(f"Intensidade Musical: {intensity}%")
    print(f"Modo Musical: {mood}")

    print("\n🎵 Render baseado em snapshot evoluído.")


if __name__ == "__main__":
    main()
