import subprocess
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def run(title, module):

    print("\n==================================================")
    print(title)
    print("==================================================\n")

    subprocess.run(
        ["python3", "-m", module],
        cwd=BASE_PATH
    )


def main():

    print("\nBITCOIN ORGANISM — AUTONOMOUS ENGINE")
    print("==================================================")

    run("Evolution Live Radar", "engine.evolution_live_radar_engine")

    run("Evolution Pressure Engine", "engine.evolution_pressure_engine")

    run("Evolution Pressure Plot", "engine.evolution_pressure_plot_engine")

    run("Evolution Atlas", "engine.evolution_atlas_engine")

    run("Evolution Memory", "engine.evolution_memory_engine")

    run("Future Path Analysis", "engine.evolution_future_path_engine")

    run("Evolution Probability", "engine.evolution_probability_engine")

    run("Evolution Scenarios", "engine.evolution_scenarios_engine_v2")

    run("Critical Transition Detector", "engine.critical_transition_engine")

    run("System Resilience", "engine.resilience_engine")

    run("Health Index", "engine.organism_health_engine")

    run("Monte Carlo Simulation", "engine.evolution_monte_carlo_engine")

    run("Trajectory Cone", "engine.evolution_trajectory_cone_engine")

    run("BTCONIC Bridge", "engine.btconic_bridge_engine")

    print("\n==================================================")
    print("Bitcoin Organism cycle complete.")
    print("==================================================\n")


if __name__ == "__main__":
    main()
