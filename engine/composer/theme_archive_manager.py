import json
import uuid
from pathlib import Path
from datetime import datetime
from engine.composer.theme_similarity_engine import build_embedding


ARCHIVE_PATH = Path("engine/composer/theme_archive.json")


# --------------------------------------------------
# Internal Utilities
# --------------------------------------------------

def _load_archive():

    if ARCHIVE_PATH.exists():
        with open(ARCHIVE_PATH, "r") as f:
            return json.load(f)

    return []


def _save_archive(archive):

    ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(ARCHIVE_PATH, "w") as f:
        json.dump(archive, f, indent=4)


# --------------------------------------------------
# Public API
# --------------------------------------------------

def register_new_theme(snapshot):

    archive = _load_archive()

    theme_id = str(uuid.uuid4())

    entry = {
        "theme_id": theme_id,
        "created_at": datetime.utcnow().isoformat(),
        "generation": 1,
        "embedding": build_embedding(snapshot).tolist(),
        "snapshot": snapshot
    }

    archive.append(entry)
    _save_archive(archive)

    return entry


def update_theme(theme_id, snapshot):

    archive = _load_archive()

    for entry in archive:

        if entry["theme_id"] == theme_id:

            entry["generation"] += 1
            entry["embedding"] = build_embedding(snapshot).tolist()
            entry["snapshot"] = snapshot
            entry["updated_at"] = datetime.utcnow().isoformat()

            break

    _save_archive(archive)


def get_all_themes():

    return _load_archive()


def get_theme_by_id(theme_id):

    archive = _load_archive()

    for entry in archive:
        if entry["theme_id"] == theme_id:
            return entry

    return None
