import json
import numpy as np
from pathlib import Path


ARCHIVE_PATH = Path("engine/composer/theme_archive.json")


# --------------------------------------------------
# Embedding Builder
# --------------------------------------------------

def build_embedding(theme_snapshot):
    """
    Constrói vetor numérico simples baseado no estado musical.
    """

    return np.array([
        float(theme_snapshot.get("risk_score", 0.0)),
        float(theme_snapshot.get("regime_confidence", 0.0)),
        float(theme_snapshot.get("volatility_score", 0.0)),
        float(theme_snapshot.get("profile", {}).get("tension_base", 0.0)),
        float(theme_snapshot.get("profile", {}).get("density", 0.0)),
        float(theme_snapshot.get("harmony", {}).get("tension", 0.0)),
    ])


# --------------------------------------------------
# Distance Calculation
# --------------------------------------------------

def euclidean_distance(v1, v2):
    return np.linalg.norm(v1 - v2)


# --------------------------------------------------
# Similarity Engine
# --------------------------------------------------

def compute_similarity(current_snapshot):

    if not ARCHIVE_PATH.exists():
        return {
            "match_found": False,
            "reason": "archive_not_found"
        }

    with open(ARCHIVE_PATH, "r") as f:
        archive = json.load(f)

    if not archive:
        return {
            "match_found": False,
            "reason": "archive_empty"
        }

    current_vector = build_embedding(current_snapshot)

    distances = []

    for entry in archive:

        past_vector = build_embedding(entry["snapshot"])
        distance = euclidean_distance(current_vector, past_vector)

        distances.append({
            "theme_id": entry["theme_id"],
            "distance": float(round(distance, 6))
        })

    distances.sort(key=lambda x: x["distance"])

    best = distances[0]

    # Similarity score invertido (0 distante → 1 idêntico)
    max_distance = max(d["distance"] for d in distances) + 1e-8
    similarity_score = 1 - (best["distance"] / max_distance)

    return {
        "match_found": True,
        "best_match_theme_id": best["theme_id"],
        "distance": best["distance"],
        "similarity_score": round(float(similarity_score), 4)
    }
