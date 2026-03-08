import subprocess
import sys

print("🧬 BITCOIN ORGANISM — EXECUÇÃO TOTAL")


def run_step(module_path, label):
    print(f"\n▶ {label}")
    result = subprocess.run(
        f"python3 -m {module_path}",
        shell=True
    )
    if result.returncode != 0:
        print(f"❌ Falha em: {label}")
        sys.exit(1)


def main():
    evolve_flag = "--evolve" in sys.argv

    # 1 — Pipeline Diário
    run_step(
        "engine.market.run_daily_pipeline",
        "Pipeline Diário"
    )

    # 2 — Atualização Regime
    run_step(
        "engine.market.validators.persist_regime_state",
        "Atualização Regime"
    )

    # 3 — Cálculo Alocação
    run_step(
        "engine.market.allocation.regime_allocation",
        "Cálculo Alocação"
    )

    print("\n✅ ORGANISMO BASE ATIVO")

    # 4 — BTConic
    run_step(
        "engine.music.regime_to_btconic",
        "BTConic — Motor Musical"
    )

    # 5 — Evolução opcional
    if evolve_flag:
        print("\n🧠 EVOLUTION MODE ATIVADO")
        run_step(
            "engine.evolution.evolutionary_controller",
            "Controlador Evolutivo"
        )

        # Render a partir do snapshot evoluído
        run_step(
            "engine.music.render_from_snapshot",
            "Render Evoluído"
        )
    else:
        print("\n🎵 MODO PADRÃO (sem evolução)")


if __name__ == "__main__":
    main()
