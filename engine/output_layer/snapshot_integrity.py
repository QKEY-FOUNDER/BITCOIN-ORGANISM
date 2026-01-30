# engine/output_layer/snapshot_integrity.py

import hashlib
from pathlib import Path


def calculate_hash(file_path: Path) -> str:
    """
    Calcula SHA-256 do conteúdo bruto do ficheiro.
    """
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_snapshot_integrity(snapshot_file: Path, hash_file: Path) -> dict:
    """
    Verifica integridade entre snapshot e hash guardado.
    Retorna resultado canónico, sem efeitos colaterais.
    """
    if not snapshot_file.exists():
        return {
            "integrity": "missing",
            "reason": "snapshot_file_not_found",
        }

    if not hash_file.exists():
        return {
            "integrity": "missing",
            "reason": "hash_file_not_found",
        }

    current_hash = calculate_hash(snapshot_file)
    stored_hash = hash_file.read_text().strip()

    if current_hash == stored_hash:
        return {
            "integrity": "ok",
            "hash": current_hash,
        }

    return {
        "integrity": "broken",
        "expected": stored_hash,
        "found": current_hash,
    }
