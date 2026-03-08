import json
import uuid
from pathlib import Path
from datetime import datetime

ARCHIVE_PATH = Path("data/theme_registry.json")


def load_archive():
    if ARCHIVE_PATH.exists():
        with open(ARCHIVE_PATH, "r") as f:
            return json.load(f)
    return []


def save_archive(archive):
    ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVE_PATH, "w") as f:
        json.dump(archive, f, indent=4)


def create_theme(theme_data):
    archive = load_archive()

    theme_data["theme_id"] = str(uuid.uuid4())
    theme_data["created_at"] = datetime.utcnow().isoformat()
    theme_data["generation"] = 1

    archive.append(theme_data)
    save_archive(archive)

    return theme_data


def update_theme(theme_id, updated_data):
    archive = load_archive()

    for theme in archive:
        if theme["theme_id"] == theme_id:
            theme.update(updated_data)
            theme["generation"] += 1
            break

    save_archive(archive)
