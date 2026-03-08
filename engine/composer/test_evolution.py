import copy
from engine.composer.evolutionary_controller import evolve_snapshot


def create_base_snapshot():

    return {
        "risk_score": 0.4,
        "regime_confidence": 0.7,
        "volatility_score": 0.6,
        "profile": {
            "tension_base": 0.5,
            "density": 0.6
        },
        "harmony": {
            "tension": 0.55
        }
    }


def run_test():

    print("\n--- TESTE 1: PRIMEIRO SNAPSHOT ---")
    base = create_base_snapshot()
    evolved1 = evolve_snapshot(base)
    print(evolved1)

    print("\n--- TESTE 2: SNAPSHOT SEMELHANTE (micro mutação esperada) ---")
    similar = copy.deepcopy(base)
    similar["risk_score"] += 0.01
    evolved2 = evolve_snapshot(similar)
    print(evolved2)

    print("\n--- TESTE 3: SNAPSHOT DIFERENTE (nova identidade esperada) ---")
    different = create_base_snapshot()
    different["risk_score"] = 0.9
    different["volatility_score"] = 0.95
    evolved3 = evolve_snapshot(different)
    print(evolved3)


if __name__ == "__main__":
    run_test()
