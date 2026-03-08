# engine/output_layer/symbolic_signature.py

from pathlib import Path
import hashlib


ORGANISM_ID = "bitcoin-organism"
CYCLE_VERSION = "cycle:v1"


def sign_snapshot(snapshot_path: str) -> str:
    """
    Cria uma assinatura simbólica para o snapshot diário.
    A assinatura não altera o snapshot — apenas o sela.
    """

    snapshot_path = Path(snapshot_path)
    hash_path = snapshot_path.with_suffix(".sha256")
    sig_path = snapshot_path.with_suffix(".sig")

    if not hash_path.exists():
        raise FileNotFoundError("Hash do snapshot não encontrado.")

    if sig_path.exists():
        return str(sig_path)

    snapshot_hash = hash_path.read_text().strip()

    symbolic_payload = f"{snapshot_hash}|{ORGANISM_ID}|{CYCLE_VERSION}"

    signature = hashlib.sha256(
        symbolic_payload.encode("utf-8")
    ).hexdigest()

    sig_path.write_text(signature, encoding="utf-8")

    return str(sig_path)
