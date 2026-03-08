from engine.composer.theme_similarity_engine import compute_similarity
from engine.composer.mutation_engine import mutate_snapshot
from engine.composer.theme_archive_manager import (
    register_new_theme,
    update_theme,
    get_theme_by_id
)


# --------------------------------------------------
# Evolution Controller
# --------------------------------------------------

def evolve_snapshot(snapshot):

    similarity = compute_similarity(snapshot)

    # Se não há histórico, regista como primeiro tema
    if not similarity.get("match_found"):
        register_new_theme(snapshot)
        return snapshot

    similarity_score = similarity["similarity_score"]
    theme_id = similarity["best_match_theme_id"]

    # Mutar snapshot baseado na similaridade
    evolved_snapshot = mutate_snapshot(snapshot, similarity_score)

    # Atualizar tema existente
    update_theme(theme_id, evolved_snapshot)

    return evolved_snapshot
