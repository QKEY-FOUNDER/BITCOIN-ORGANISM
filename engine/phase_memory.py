import json
import os
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent.parent
HISTORY_PATH = BASE_PATH / "data" / "phase_history" / "market_phase_history.json"


def load_history():
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def update_phase_history(month, phase, metrics, acceleration):

    history = load_history()

    entry = {
        "month": month,
        "phase": phase,
        "structural_tension": metrics["structural_tension"],
        "volatility_resonance": metrics["volatility_resonance"],
        "volatility_acceleration": acceleration["volatility_acceleration"]
    }

    history.append(entry)

    save_history(history)

    return history


def compute_regime_duration(history):

    if not history:
        return 0

    last_phase = history[-1]["phase"]
    duration = 0

    for entry in reversed(history):
        if entry["phase"] == last_phase:
            duration += 1
        else:
            break

    return duration
