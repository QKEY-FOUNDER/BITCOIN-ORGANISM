import json
from pathlib import Path


def seal_snapshot(canonical_state: dict) -> None:
    """
    Snapshot Seal Layer
    Sela o estado canónico diário como memória persistente.
    Append-only. Nunca sobrescreve.
    """

    if not canonical_state or "date" not in canonical_state:
        print("⚠️ Snapshot não selado: estado inválido.")
        return

    base_dir = Path("data/07_global_reckoning_2022_infinity/snapshots/daily")
    base_dir.mkdir(parents=True, exist_ok=True)

    date_str = canonical_state["date"]
    snapshot_file = base_dir / f"{date_str}.json"

    if snapshot_file.exists():
        print(f"🧠 Snapshot já existe para {date_str} — preservado.")
        return

    with open(snapshot_file, "w") as f:
        json.dump(canonical_state, f, indent=2)

    print(f"🧬 Snapshot selado: {snapshot_file}")
