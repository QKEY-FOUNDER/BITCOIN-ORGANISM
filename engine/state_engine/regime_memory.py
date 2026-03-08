import json
import math
from pathlib import Path


# =========================================================
# REGIME MEMORY — Persistência Temporal
# Consolidação logística contínua
# =========================================================

BASE_PATH = Path(__file__).resolve().parents[2]

MEMORY_DIR = BASE_PATH / "data" / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_FILE = MEMORY_DIR / "regime_memory.json"


# ---------------------------------------------------------
# LOAD MEMORY
# ---------------------------------------------------------
def load_memory() -> dict:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------
# SAVE MEMORY
# ---------------------------------------------------------
def save_memory(memory: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


# ---------------------------------------------------------
# UPDATE REGIME MEMORY
# ---------------------------------------------------------
def update_regime_memory(canonical_state: dict) -> dict:
    """
    Atualiza persistência temporal do regime
    com maturação logística orgânica.
    """

    memory = load_memory()

    current_regime = canonical_state.get("interpretation", "neutral")
    today = canonical_state.get("date")

    # Inicialização
    if "regime" not in memory:
        memory["regime"] = {
            "value": current_regime,
            "days": 1,
            "last_date": today
        }

    # Continuidade ou reset
    else:
        if memory["regime"]["value"] == current_regime:
            memory["regime"]["days"] += 1
        else:
            memory["regime"]["value"] = current_regime
            memory["regime"]["days"] = 1

        memory["regime"]["last_date"] = today

    # Sensibilidade Logística
    days = memory["regime"]["days"]

    k = 0.6
    center = 6

    maturity = 1 / (1 + math.exp(-k * (days - center)))

    memory["regime"]["stability_ratio"] = round(maturity, 4)

    save_memory(memory)

    return memory
