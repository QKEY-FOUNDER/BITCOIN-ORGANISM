# engine/output_layer/snapshot_writer.py

from pathlib import Path
import json
import hashlib
from datetime import date


def _to_python(obj):
    """
    Converte tipos numpy / pandas em tipos Python puros.
    """
    try:
        import numpy as np
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
    except Exception:
        pass

    if isinstance(obj, dict):
        return {k: _to_python(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_python(v) for v in obj]

    return obj


def write_daily_snapshot(
    canonical_state: dict,
    health_state: dict,
    immune: dict,
    output: dict,
):
    """
    Escreve o batimento diário do organismo.
    Snapshot imutável + hash SHA256.
    """

    today = canonical_state.get("date") or date.today().isoformat()

    base_dir = Path("data/output/heartbeat")
    base_dir.mkdir(parents=True, exist_ok=True)

    snapshot_path = base_dir / f"{today}.json"
    hash_path = base_dir / f"{today}.sha256"

    if snapshot_path.exists():
        return str(snapshot_path)

    snapshot = {
        "date": today,
        "canonical_state": _to_python(canonical_state),
        "health": _to_python(health_state),
        "immune": _to_python(immune),
        "output": _to_python(output),
    }

    payload = json.dumps(
        snapshot,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    )

    snapshot_path.write_text(payload, encoding="utf-8")

    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    hash_path.write_text(digest, encoding="utf-8")

    return str(snapshot_path)
