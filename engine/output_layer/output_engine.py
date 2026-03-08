"""
OUTPUT ENGINE — Camada de Expressão
Converte estado canónico em estrutura expressiva.
Nenhuma decisão estrutural.
Apenas tradução estado → forma.
"""

from engine.output_layer.btconic_contract import btconic_contract


def render_output(canonical_state: dict, health_state=None, immune=None) -> dict:
    """
    Output Layer — Expressão pura.
    """

    if not canonical_state:
        return {
            "mode": "silent",
            "intensity": 0.0,
            "expression": "none",
            "regime": "unknown",
        }

    # Traduz fisiologia em parâmetros primitivos
    contract = btconic_contract(canonical_state)

    # Base estrutural
    frame = {
        "date": canonical_state.get("date"),
        "mode": contract.get("mode"),
        "expression": contract.get("expression"),
        "regime": canonical_state.get("regime"),
        "regime_duration": canonical_state.get("regime_duration"),
    }

    # ==============================
    # ESTABILIDADE CONTÍNUA
    # ==============================
    stability_ratio = canonical_state.get("stability_ratio", 0.0)
    frame["stability_ratio"] = stability_ratio

    # Intensidade contínua (0.2 base → 1.0 máximo)
    base_intensity = 0.2
    frame["intensity"] = round(base_intensity + (0.8 * stability_ratio), 3)

    # Densidade progressiva
    if stability_ratio < 0.3:
        frame["density"] = "minimal"
    elif stability_ratio < 0.6:
        frame["density"] = "moderate"
    else:
        frame["density"] = "expanded"

    # Harmonic mode contínuo
    frame["harmonic_mode"] = (
        "floating" if stability_ratio < 0.6 else "coherent"
    )

    # ==============================
    # ENRIQUECIMENTO CONTEXTUAL
    # ==============================
    if health_state:
        frame["health_state"] = health_state

    if immune:
        frame["immune_action"] = immune.get("action")
        frame["immune_status"] = immune.get("status")

    return frame
