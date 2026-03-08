import json
from pathlib import Path


def export_snapshot(
    date,
    close_price,
    regime,
    btc_weight,
    cash_weight,
    risk_score,
    stress_trend="flat",
    volatility_score=0.0,
):

    snapshot = {
        "date": str(date),
        "regime": regime,
        "btc_price": float(close_price),
        "allocation": {
            "BTC_Weight": float(btc_weight),
            "Cash_Weight": float(cash_weight),
        },
        "risk_state": {
            "risk_score": float(risk_score),
            "stress_trend": stress_trend,
            "volatility_score": float(volatility_score),
        },
    }

    # -------------------------------------------------------
    # Current Snapshot (Single Source of Truth)
    # -------------------------------------------------------

    current_path = Path("data/organism_snapshot.json")
    current_path.parent.mkdir(parents=True, exist_ok=True)

    with open(current_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    # -------------------------------------------------------
    # Historical Snapshot (Immutable Archive)
    # -------------------------------------------------------

    history_dir = Path("data/organism_history")
    history_dir.mkdir(parents=True, exist_ok=True)

    historical_path = history_dir / f"{snapshot['date']}.json"

    with open(historical_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print("Organism snapshot exported successfully.")
    print(f"Current: {current_path}")
    print(f"Historical: {historical_path}")
