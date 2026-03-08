from pathlib import Path
import pandas as pd
import json
import random
import numpy as np

print("BTCONIC v5 - Hybrid Risk Engine (Evolutive)")


def main():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DATA_DIR = PROJECT_ROOT / "data" / "market"

    OUTPUT_FILE = DATA_DIR / "output" / "btconic_state.json"

    # --- SNAPSHOT SELECTION ---
    BASE_SNAPSHOT = PROJECT_ROOT / "data" / "organism_snapshot.json"
    EVOLVED_SNAPSHOT = PROJECT_ROOT / "data" / "organism_snapshot_evolved.json"

    if EVOLVED_SNAPSHOT.exists():
        SNAPSHOT_FILE = EVOLVED_SNAPSHOT
    else:
        SNAPSHOT_FILE = BASE_SNAPSHOT

    FUSED_FILE = DATA_DIR / "final" / "btc_daily_full.csv"
    REGIME_FILE = DATA_DIR / "output" / "regime_state.csv"
    ALLOCATION_FILE = DATA_DIR / "output" / "allocation_state.csv"

    if not FUSED_FILE.exists() or not REGIME_FILE.exists():
        raise RuntimeError("Dados insuficientes")

    fused = pd.read_csv(FUSED_FILE, parse_dates=["Date"])
    regime_df = pd.read_csv(REGIME_FILE)

    latest_regime = regime_df.iloc[-1]["regime"]
    stress = float(regime_df.iloc[-1]["stress_ewma"])

    # -------------------------
    # Stress Trend
    # -------------------------
    if len(regime_df) > 1:
        prev_stress = float(regime_df.iloc[-2]["stress_ewma"])
        stress_velocity = stress - prev_stress
    else:
        stress_velocity = 0.0

    if stress_velocity > 0.01:
        stress_trend = "up"
    elif stress_velocity < -0.01:
        stress_trend = "down"
    else:
        stress_trend = "flat"

    # -------------------------
    # Volatility Score
    # -------------------------
    fused["return"] = fused["Close"].pct_change()
    volatility = fused["return"].rolling(7).std().iloc[-1]

    if np.isnan(volatility):
        volatility = 0.0

    volatility_score = min(float(volatility) * 50, 1.0)

    # -------------------------
    # Risk Score
    # -------------------------
    risk_score = (
        0.5 * min(stress, 1.0)
        + 0.3 * min(abs(stress_velocity) * 5, 1.0)
        + 0.2 * volatility_score
    )

    risk_score = round(min(risk_score, 1.0), 3)
    regime_confidence = round(1 - risk_score, 3)

    # -------------------------
    # Musical Layer
    # -------------------------
    major_scale = ["C", "D", "E", "F", "G", "A", "B"]
    minor_scale = ["C", "D", "Eb", "F", "G", "Ab", "Bb"]

    if latest_regime == "calm":
        scale = major_scale
        base_bpm = 60
    elif latest_regime == "volatile":
        scale = minor_scale
        base_bpm = 90
    else:
        scale = minor_scale[::-1]
        base_bpm = 110

    prev_bpm = base_bpm
    prev_note = scale[0]
    prev_dissonance = 0.0

    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r") as f:
                previous = json.load(f)
                prev_bpm = previous.get("bpm", base_bpm)
                prev_notes = previous.get("notes", [scale[0]])
                if prev_notes:
                    prev_note = prev_notes[-1]
                prev_dissonance = previous.get("dissonance", 0.0)
        except:
            pass

    bpm = int(prev_bpm * 0.7 + base_bpm * 0.3)

    if prev_note in scale:
        start_index = scale.index(prev_note)
    else:
        start_index = 0

    notes = []
    for i in range(8):
        idx = (start_index + i) % len(scale)
        notes.append(scale[idx])

    dissonance = round(prev_dissonance * 0.6 + risk_score, 2)

    if risk_score > 0.6:
        notes[random.randint(0, 7)] = "F#"

    intensity = round(risk_score, 3)

    # -----------------------------------
    # Mutation Bias Modulation (REAL)
    # -----------------------------------
    mutation_bias = None

    if SNAPSHOT_FILE.exists():
        try:
            with open(SNAPSHOT_FILE, "r") as f:
                snapshot = json.load(f)
                risk_state = snapshot.get("risk_state", {})
                mutation_bias = risk_state.get("mutation_bias")
        except:
            pass

    if mutation_bias:
        print(f"🧬 Mutation bias ativo: {mutation_bias}")

        if mutation_bias == "expansion":
            bpm = int(bpm * 1.15)
            intensity = min(intensity + 0.1, 1.0)

        elif mutation_bias == "defensive":
            bpm = int(bpm * 0.85)
            dissonance = round(dissonance * 0.5, 2)

        elif mutation_bias == "chaotic":
            bpm = int(bpm * 1.25)
            dissonance = min(dissonance + 0.3, 1.0)

    # -------------------------
    # Final State
    # -------------------------
    state = {
        "regime": latest_regime,
        "scale": scale,
        "bpm": bpm,
        "intensity": intensity,
        "dissonance": dissonance,
        "notes": notes,
        "risk_score": risk_score,
        "stress_trend": stress_trend,
        "volatility_score": volatility_score,
        "regime_confidence": regime_confidence,
        "mutation_bias": mutation_bias,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(state, f, indent=4)

    print("Estado musical + risco gerado")
    print(state)
    print("ORGANISMO HÍBRIDO ATIVO")


if __name__ == "__main__":
    main()
