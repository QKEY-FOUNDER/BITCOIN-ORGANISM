#!/bin/bash

echo "=================================================="
echo "BITCOIN ORGANISM — FULL SYSTEM EXECUTION"
echo "=================================================="

echo ""
echo "1 — Market Sensors"
echo "--------------------------------------------------"

python3 -m engine.market_data_sensor_engine
python3 -m engine.physiology_generator_engine
python3 -m engine.rolling_physiology_engine

echo ""
echo "2 — Evolution Engines"
echo "--------------------------------------------------"

python3 -m engine.evolution_live_radar_engine
python3 -m engine.evolution_pressure_engine
python3 -m engine.evolution_memory_engine
python3 -m engine.evolution_future_path_engine
python3 -m engine.evolution_probability_engine
python3 -m engine.evolution_scenarios_engine_v2

echo ""
echo "3 — System Stability"
echo "--------------------------------------------------"

python3 -m engine.critical_transition_engine
python3 -m engine.resilience_engine
python3 -m engine.organism_health_engine

echo ""
echo "4 — Simulations"
echo "--------------------------------------------------"

python3 -m engine.evolution_monte_carlo_engine
python3 -m engine.evolution_trajectory_cone_engine

echo ""
echo "5 — Intelligence Layer"
echo "--------------------------------------------------"

python3 -m engine.cycle_phase_engine
python3 -m engine.evolution_intelligence_engine
python3 -m engine.evolution_consciousness_engine

echo ""
echo "6 — Learning Layer"
echo "--------------------------------------------------"

python3 -m engine.evolution_learning_engine
python3 -m engine.adaptive_model_engine
python3 -m engine.evolution_reflex_engine
python3 -m engine.evolution_meta_intelligence_engine
python3 -m engine.evolution_self_calibration_engine

echo ""
echo "7 — Historical Engines"
echo "--------------------------------------------------"

python3 -m engine.evolution_era_detector_engine
python3 -m engine.evolution_time_machine_engine
python3 -m engine.evolution_historical_outcomes_engine

echo ""
echo "8 — Visualization Engines"
echo "--------------------------------------------------"

python3 -m engine.evolution_pressure_plot_engine
python3 -m engine.evolution_atlas_engine
python3 -m engine.evolution_timeline_engine
python3 -m engine.evolution_climate_engine
python3 -m engine.evolution_dashboard_engine

echo ""
echo "9 — Opening Maps"
echo "--------------------------------------------------"

open data/evolution_pressure_plot.png
open data/bitcoin_evolution_atlas.png
open data/evolution_trajectory_cone.png
open data/bitcoin_evolution_timeline.png
open data/bitcoin_evolution_climate.png
open data/bitcoin_organism_dashboard.png

echo ""
echo "=================================================="
echo "BITCOIN ORGANISM — EXECUTION COMPLETE"
echo "=================================================="
