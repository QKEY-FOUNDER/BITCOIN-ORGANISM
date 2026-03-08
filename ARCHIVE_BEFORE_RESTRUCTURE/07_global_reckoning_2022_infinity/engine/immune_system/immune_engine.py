from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

print("🧬 IMMUNE ENGINE — REGULAÇÃO")

def immune_response(
    price_state: str,
    macro_state: str,
    geo_state: str,
    health_state: str,
):
    """
    Decide a resposta imunitária do organismo
    com base no estado canónico e na saúde.
    """

    if health_state != "healthy":
        return {
            "status": "protect",
            "action": "observe_only",
            "expression": "minimal",
            "reason": "health_not_healthy",
        }

    if geo_state == "geo_silent":
        return {
            "status": "watch",
            "action": "observe_only",
            "expression": "neutral",
            "reason": "geo_silent_is_valid",
        }

    return {
        "status": "active",
        "action": "allow",
        "expression": "full",
        "reason": "stable_conditions",
    }
