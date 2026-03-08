from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

print("🧬 IMMUNE ENGINE — REGULAÇÃO")

def immune_response(
    price_state: str,
    macro_state: str,
    geo_state: str,
    health_state: str,
    stability_ratio: float = 0.0,
):
    """
    Decide a resposta imunitária do organismo
    com base no estado canónico, saúde e maturidade estrutural.
    """

    # ==========================================================
    # 1️⃣ CAMADA PRIMÁRIA — SAÚDE DO ORGANISMO
    # ==========================================================
    if health_state != "healthy":
        return {
            "status": "protect",
            "action": "observe_only",
            "expression": "minimal",
            "reason": "health_not_healthy",
            "stability_ratio": stability_ratio,
        }

    # ==========================================================
    # 2️⃣ CAMADA GEO — SILÊNCIO GEOPOLÍTICO
    # ==========================================================
    if geo_state == "geo_silent":
        return {
            "status": "watch",
            "action": "observe_only",
            "expression": "neutral",
            "reason": "geo_silent_is_valid",
            "stability_ratio": stability_ratio,
        }

    # ==========================================================
    # 3️⃣ CAMADA HARMÓNICA — MATURIDADE DO REGIME
    # ==========================================================
    if stability_ratio < 0.4:
        maturity_status = "cautious"
        intensity = "low"

    elif 0.4 <= stability_ratio < 0.7:
        maturity_status = "transitional"
        intensity = "medium"

    else:
        maturity_status = "confirmed"
        intensity = "high"

    # ==========================================================
    # 4️⃣ INTERPRETAÇÃO DE PREÇO + MACRO
    # ==========================================================
    if price_state == "expansion" and macro_state != "risk_off":
        action = "expand"

    elif price_state == "contraction":
        action = "defend"

    else:
        action = "observe"

    return {
        "status": maturity_status,
        "action": action,
        "expression": intensity,
        "reason": "weighted_by_stability",
        "stability_ratio": stability_ratio,
    }
