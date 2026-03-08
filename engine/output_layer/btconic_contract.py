"""
BTConic Contract
Traduz estado canónico em parâmetros expressivos primários.
"""

def btconic_contract(state: dict) -> dict:
    """
    Tradução fisiologia → vibração.
    """

    if not state:
        return {}

    stability_ratio = state.get("stability_ratio", 0.0)

    # Intensidade proporcional à maturidade do regime
    intensity = round(0.2 + (0.8 * stability_ratio), 3)

    # Modo tonal depende do regime
    regime = state.get("regime", "unknown")

    if regime in ["expansion", "bull", "macro_expansion"]:
        mode = "major"
    else:
        mode = "minor"

    expression = state.get("immune_action", "observe_only")

    return {
        "mode": mode,
        "intensity": intensity,
        "expression": expression,
    }
