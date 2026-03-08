# engine/output_layer/heartbeat_writer.py

from pathlib import Path
from datetime import datetime, timezone


def write_heartbeat(
    date: str,
    health_state: str,
    immune_action: str,
    snapshot_file: str,
):
    """
    Escreve um batimento diário append-only.
    Nunca lê. Nunca corrige. Nunca decide.
    """

    base_path = Path(__file__).resolve().parents[2]
    log_dir = base_path / "data" / "output"
    log_dir.mkdir(parents=True, exist_ok=True)

    heartbeat_file = log_dir / "heartbeat.log"

    timestamp = datetime.now(timezone.utc).isoformat()

    line = (
        f"{timestamp} | "
        f"date={date} | "
        f"health={health_state} | "
        f"immune_action={immune_action} | "
        f"snapshot={snapshot_file}\n"
    )

    with open(heartbeat_file, "a", encoding="utf-8") as f:
        f.write(line)

    return str(heartbeat_file)
