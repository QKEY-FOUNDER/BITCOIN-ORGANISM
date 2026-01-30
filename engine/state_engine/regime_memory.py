# engine/state_engine/regime_memory.py

from pathlib import Path
import json


REGIME_KEYS = [
    "price_state",
    "macro_state",
    "geo_state",
    "interpretation",
]


def update_regime_memory(canonical_state: dict):
    """
    Mantém memória de regimes persistentes.
    Conta N dias consecutivos no mesmo estado.
    """

    base_path = Path(__file__).resolve().parents[2]
    memory_dir = base_path / "data" / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    memory_file = memory_dir / "regime_memory.json"

    today = canonical_state["date"]

    if memory_file.exists():
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
    else:
        memory = {}

    updated = {}

    for key in REGIME_KEYS:
        value = canonical_state.get(key)

        previous = memory.get(key)

        if previous and previous["value"] == value:
            updated[key] = {
                "value": value,
                "days": previous["days"] + 1,
                "since": previous["since"],
            }
        else:
            updated[key] = {
                "value": value,
                "days": 1,
                "since": today,
            }

    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)

    return updated
