from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

print("🔊 OUTPUT LAYER — EXPRESSÃO CONSCIENTE")

def render_output(
    canonical_state: dict,
    health_state: str,
    immune: dict,
):
    """
    Camada de expressão do organismo.
    Apenas leitura. A expressão varia conforme saúde e ação imunitária.
    """

    price_state = canonical_state.get("price_state")
    macro_state = canonical_state.get("macro_state")
    geo_state = canonical_state.get("geo_state")
    interpretation = canonical_state.get("interpretation")

    action = immune.get("action", "observe_only")
    expression = immune.get("expression", "neutral")

    print("\n🎼 Expressão do Organismo:")
    print(f"• Preço: {price_state}")
    print(f"• Macro: {macro_state}")
    print(f"• GEO: {geo_state}")
    print(f"• Interpretação: {interpretation}")
    print(f"• Saúde: {health_state}")
    print(f"• Ação imunitária: {action}")
    print(f"• Expressão: {expression}")

    # Expressão simbólica (placeholder evolutivo)
    if expression == "minimal":
        print("🔈 Som: pulso mínimo")
    elif expression == "neutral":
        print("🔉 Som: pulso estável")
    elif expression == "full":
        print("🔊 Som: expressão plena")
    else:
        print("🔇 Som: silêncio")

    return {
        "expression": expression,
        "action": action,
    }
