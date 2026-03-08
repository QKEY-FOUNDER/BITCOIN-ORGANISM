import os

def run(engine):

    print("\n==================================================")
    print(engine)
    print("==================================================\n")

    os.system(f"python3 -m engine.{engine}")


def main():

    print("\nBITCOIN ORGANISM — AUTONOMOUS CYCLE")
    print("==================================================")

    engines = [

        "evolution_live_radar_engine",
        "evolution_pressure_engine",
        "evolution_pressure_plot_engine",
        "evolution_timeline_engine",
        "evolution_climate_engine",
        "evolution_memory_engine",
        "evolution_future_path_engine",
        "evolution_probability_engine",
        "evolution_scenarios_engine_v2",
        "critical_transition_engine",
        "resilience_engine",
        "organism_health_engine",
        "evolution_monte_carlo_engine",
        "evolution_trajectory_cone_engine",
        "cycle_phase_engine",
        "evolution_intelligence_engine",
        "evolution_consciousness_engine",
        "evolution_era_detector_engine",
        "early_warning_engine",
        "evolution_dashboard_engine",
        "btconic_bridge_engine"

    ]

    for engine in engines:

        run(engine)

    print("\n==================================================")
    print("Bitcoin Organism autonomous cycle complete.")
    print("==================================================")


if __name__ == "__main__":
    main()
