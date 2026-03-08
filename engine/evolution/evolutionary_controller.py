from pathlib import Path
import json
import copy

print("🧠 EVOLUTIONARY CONTROLLER")


def main():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    SNAPSHOT_FILE = PROJECT_ROOT / "data" / "organism_snapshot.json"

    if not SNAPSHOT_FILE.exists():
        raise RuntimeError("Snapshot não encontrado")

    with open(SNAPSHOT_FILE, "r") as f:
        snapshot = json.load(f)

    evolved_snapshot = copy.deepcopy(snapshot)

    risk_score = snapshot["risk_state"]["risk_score"]
    regime = snapshot["regime"]

    # -------------------------
    # Estratégia evolutiva simples
    # -------------------------
    mutation_flag = False

    if risk_score > 0.7:
        evolved_snapshot["risk_state"]["mutation_bias"] = "defensive"
        mutation_flag = True

    elif risk_score < 0.2:
        evolved_snapshot["risk_state"]["mutation_bias"] = "expansion"
        mutation_flag = True

    else:
        evolved_snapshot["risk_state"]["mutation_bias"] = "neutral"

    # Adiciona versão evolutiva
    evolved_snapshot["evolution"] = {
        "version": 1,
        "mutation_applied": mutation_flag
    }

    # Guardar snapshot evoluído
    EVOLVED_FILE = PROJECT_ROOT / "data" / "organism_snapshot_evolved.json"

    with open(EVOLVED_FILE, "w") as f:
        json.dump(evolved_snapshot, f, indent=4)

    print("🧬 Snapshot evoluído gerado.")
    print("Mutação aplicada:", mutation_flag)


if __name__ == "__main__":
    main()
