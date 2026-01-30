# =========================================================
# IMMUNE SYSTEM — Bitcoin Organism
# Deteta fragilidade cognitiva, não corrige dados
# =========================================================

print("🛡️ IMMUNE SYSTEM — ACTIVE (READ-ONLY)")
print("=" * 50)

# ---------------------------------------------------------
# IMMUNE RESPONSE TO STATES
# ---------------------------------------------------------

def immune_response(canonical_state):
    """
    Recebe o estado canónico do State Engine
    e devolve:
    - immune_flags
    - modifiers
    """

    immune_flags = []
    modifiers = {
        "confidence": 1.0,
        "aggression": 1.0,
        "volatility": 1.0
    }

    geo_mode = canonical_state.get("geo_mode")
    macro_state = canonical_state.get("macro_state")

    # -----------------------------------------------------
    # GEO BLINDNESS
    # -----------------------------------------------------

    if geo_mode == "silent":
        immune_flags.append("geo_blind")

        modifiers["confidence"] *= 0.7
        modifiers["aggression"] *= 0.6
        modifiers["volatility"] *= 0.8

    # -----------------------------------------------------
    # MACRO BLINDNESS (Dominance ausente)
    # -----------------------------------------------------

    if macro_state == "no_dominance":
        immune_flags.append("macro_blind")

        modifiers["confidence"] *= 0.8
        modifiers["aggression"] *= 0.7

    # -----------------------------------------------------
    # COMBINED BLINDNESS (perigoso)
    # -----------------------------------------------------

    if "geo_blind" in immune_flags and "macro_blind" in immune_flags:
        immune_flags.append("systemic_blindness")

        modifiers["confidence"] *= 0.6
        modifiers["aggression"] *= 0.5
        modifiers["volatility"] *= 0.7

    return {
        "immune_flags": immune_flags,
        "modifiers": modifiers
    }

# ---------------------------------------------------------
# OBSERVATION MODE OUTPUT
# ---------------------------------------------------------

def print_immune_status(immune_state):
    print("\n🧬 Estado Imunitário:")
    
    flags = immune_state["immune_flags"]
    mods  = immune_state["modifiers"]

    if not flags:
        print(" • Sistema estável")
    else:
        for f in flags:
            print(f" • Flag ativa: {f}")

    print("\n🛠️ Modificadores ativos:")
    for k, v in mods.items():
        print(f" • {k}: {v}")

    print("\nℹ️ Immune System em modo observação.")
