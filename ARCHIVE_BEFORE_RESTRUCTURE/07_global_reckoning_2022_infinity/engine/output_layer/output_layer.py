# =========================================================
# OUTPUT LAYER — Bitcoin Organism
# Expressão sensorial (som / estado / silêncio)
# =========================================================

print("🔊 OUTPUT LAYER — ACTIVE (READ-ONLY)")
print("=" * 50)

# ---------------------------------------------------------
# OUTPUT RESOLVER
# ---------------------------------------------------------

def resolve_output(canonical_state, immune_state, geo_state):
    """
    Recebe:
    - canonical_state (State Engine)
    - immune_state (Immune System)
    - geo_state (Geo Engine)

    Devolve um output sensorial abstrato
    (não gera som físico — apenas estado)
    """

    output = {
        "mode": None,
        "intensity": 0.0,
        "texture": None,
        "comment": None
    }

    immune_flags = immune_state.get("immune_flags", [])
    geo_mode     = geo_state.get("mode")

    # -----------------------------------------------------
    # SILÊNCIO ABSOLUTO
    # -----------------------------------------------------

    if "systemic_blindness" in immune_flags:
        output.update({
            "mode": "silence",
            "intensity": 0.0,
            "texture": "void",
            "comment": "Systemic blindness — organism retreats"
        })
        return output

    # -----------------------------------------------------
    # GEO SILENT (memória acabou)
    # -----------------------------------------------------

    if geo_mode == "silent":
        output.update({
            "mode": "ambient_drone",
            "intensity": 0.2,
            "texture": "low_frequency",
            "comment": "Geo silent — ambient awareness only"
        })
        return output

    # -----------------------------------------------------
    # NORMAL OPERATION
    # -----------------------------------------------------

    price_state = canonical_state.get("price_state")
    macro_state = canonical_state.get("macro_state")

    base_intensity = 0.5

    if price_state == "expansion":
        base_intensity += 0.2
    elif price_state == "compression":
        base_intensity -= 0.2

    if macro_state == "dominance_rising":
        base_intensity += 0.1
    elif macro_state == "no_dominance":
        base_intensity -= 0.1

    # aplicar imunidade
    modifiers = immune_state.get("modifiers", {})
    base_intensity *= modifiers.get("confidence", 1.0)

    output.update({
        "mode": "active",
        "intensity": round(max(0.0, min(1.0, base_intensity)), 2),
        "texture": "harmonic_motion",
        "comment": "Normal expressive state"
    })

    return output

# ---------------------------------------------------------
# OUTPUT DISPLAY (OBSERVAÇÃO)
# ---------------------------------------------------------

def print_output(output):
    print("\n🔊 OUTPUT SENSORIAL:")
    print(f" • Modo: {output['mode']}")
    print(f" • Intensidade: {output['intensity']}")
    print(f" • Textura: {output['texture']}")
    print(f" • Nota: {output['comment']}")
    print("\nℹ️ Output Layer em modo observação.")
