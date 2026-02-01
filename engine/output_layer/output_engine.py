from engine.output_layer.btconic_contract import btconic_contract

def output_btconic(canonical_state: dict) -> dict:
    """
    Output Layer — Expressão pura.
    Nenhuma decisão. Nenhuma escrita.
    """

    frame = btconic_contract(canonical_state)

    print("🎼 BTConic — Expressão Diária")
    print(f"Data: {canonical_state.get('date')}")
    print(f"Health: {canonical_state.get('health_state')}")
    print(f"Regime: {canonical_state.get('regime')}")
    print(f"GEO: {canonical_state.get('geo_state')}")
    print(f"Immune: {canonical_state.get('immune_action')}")
    print("— Expression —")
    for k, v in frame.items():
        print(f"{k}: {v}")

    return frame
