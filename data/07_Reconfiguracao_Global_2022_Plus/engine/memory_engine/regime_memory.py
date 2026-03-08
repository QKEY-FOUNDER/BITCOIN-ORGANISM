from pathlib import Path
import json
from typing import List, Dict, Optional

class RegimeMemory:
    """
    Memória determinística de regimes.
    Detecta padrões consecutivos no canonical_state.
    """

    def __init__(self, snapshot_dir: Path, min_days: int = 3):
        self.snapshot_dir = snapshot_dir
        self.min_days = min_days

    def _load_snapshots(self) -> List[Dict]:
        files = sorted(self.snapshot_dir.glob("*.json"))
        snapshots = []

        for f in files:
            try:
                with open(f, "r") as fp:
                    snapshots.append(json.load(fp))
            except Exception:
                continue

        return snapshots

    def current_regime(self) -> Optional[Dict]:
        snapshots = self._load_snapshots()

        if len(snapshots) < self.min_days:
            return None

        recent = snapshots[-self.min_days:]

        base_signature = (
            recent[0].get("health_state"),
            recent[0].get("regime"),
        )

        for snap in recent:
            signature = (
                snap.get("health_state"),
                snap.get("regime"),
            )
            if signature != base_signature:
                return None

        return {
            "regime_signature": base_signature,
            "duration_days": self.min_days
        }
