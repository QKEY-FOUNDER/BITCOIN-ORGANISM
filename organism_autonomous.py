import subprocess
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def run_engine(title, module):

    print("\n==================================================")
    print(title)
    print("==================================================\n")

    subprocess.run(
        ["python3", "-m", module],
        cwd=BASE_PATH
    )


def main():

    print("\nBITCOIN ORGANISM — AUTONOMOUS INTELLIGENCE")
    print("==================================================")

    # Radar fisiológico
    run_engine(
        "Evolution Live Radar",
        "engine.evolution_live_radar_engine"
    )

    # Pressão evolutiva
    run_engine(
        "Evolution Pressure Engine",
        "engine.evolution_pressure_engine"
    )

    # Visualização
    run_engine(
        "Evolution Pressure Plot",
        "engine.evolution_pressure_plot_engine"
    )

    # Atlas evolutivo
    run_engine(
        "Evolution Atlas",
        "engine.evolution_atlas_engine"
    )

    # Memória
    run_engine(
        "Evolution Memory",
        "engine.evolution_memory_engine"
    )

    # Caminhos futuros
    run_engine(
        "Future Path Analysis",
        "engine.evolution_future_path_engine"
    )

    # Probabilidade evolutiva
    run_engine(
        "Evolution Probability",
        "engine.evolution_probability_engine"
    )

    # Cenários
    run_engine(
        "Evolution Scenarios",
        "engine.evolution_scenarios_engine_v2"
    )

    # Transições críticas
    run_engine(
        "Critical Transition Detector",
        "engine.critical_transition_engine"
    )

    # Resiliência
    run_engine(
        "System Resilience",
        "engine.resilience_engine"
    )

    # Health index
    run_engine(
        "Health Index",
        "engine.organism_health_engine"
    )

    # Monte Carlo
    run_engine(
        "Monte Carlo Simulation",
        "engine.evolution_monte_carlo_engine"
    )

    # Trajectory cone
    run_engine(
        "Trajectory Cone",
        "engine.evolution_trajectory_cone_engine"
    )

    # Early warning signals
    run_engine(
        "Early Warning Signals",
        "engine.evolution_early_warning_engine"
    )

    # Risk radar
    run_engine(
        "Evolution Risk Radar",
        "engine.evolution_risk_radar_engine"
    )

    # Estratégia
    run_engine(
        "Evolution Strategy",
        "engine.evolution_strategy_engine"
    )

    # Consciência evolutiva
    run_engine(
        "Evolution Consciousness",
        "engine.evolution_consciousness_engine"
    )

    # Música do mercado
    run_engine(
        "BTCONIC Bridge",
        "engine.btconic_bridge_engine"
    )

    print("\n==================================================")
    print("Bitcoin Organism cycle complete.")
    print("==================================================\n")


if __name__ == "__main__":
    main()
