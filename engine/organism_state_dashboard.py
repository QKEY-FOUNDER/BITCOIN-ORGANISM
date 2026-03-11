import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

MACRO_FILE = BASE_PATH / "data" / "macro_climate_state.json"
LIQUIDITY_FILE = BASE_PATH / "data" / "liquidity_wave_state.json"
TRANSITION_FILE = BASE_PATH / "data" / "critical_transition_state.json"
ENERGY_FILE = BASE_PATH / "data" / "evolution_energy_state.json"
MACRO_MEMORY_FILE = BASE_PATH / "data" / "macro_memory_state.json"
MACRO_ADAPT_FILE = BASE_PATH / "data" / "macro_adaptation_state.json"

OUTPUT_FILE = BASE_PATH / "data" / "organism_state_dashboard.json"


def load_json(path):

    try:

        with open(path) as f:
            return json.load(f)

    except:

        return None


def compute_ecosystem_state(macro_climate, liquidity_wave):

    if not macro_climate or not liquidity_wave:
        return "Unknown Ecosystem"

    climate = macro_climate.get("macro_climate")
    wave = liquidity_wave.get("wave_state")

    if climate == "Risk Expansion Climate" and wave == "Ongoing Liquidity Expansion":
        return "Liquidity Expansion Ecosystem"

    if climate == "Risk Contraction Climate":
        return "Liquidity Contraction Ecosystem"

    return "Balanced Ecosystem"


def compute_transition_risk(transition_state):

    if not transition_state:
        return "Unknown"

    prob = transition_state.get("transition_probability",0)

    if prob > 0.66:
        return "High Transition Risk"

    if prob > 0.33:
        return "Moderate Transition Risk"

    return "Low Transition Risk"


def main():

    print("")
    print("BITCOIN ORGANISM — INTELLIGENCE DASHBOARD")
    print("==================================================")

    macro_climate = load_json(MACRO_FILE)
    liquidity_wave = load_json(LIQUIDITY_FILE)
    transition_state = load_json(TRANSITION_FILE)
    energy_state = load_json(ENERGY_FILE)
    macro_memory = load_json(MACRO_MEMORY_FILE)
    macro_adapt = load_json(MACRO_ADAPT_FILE)

    ecosystem = compute_ecosystem_state(macro_climate, liquidity_wave)
    transition_risk = compute_transition_risk(transition_state)

    energy = None

    if energy_state:
        energy = energy_state.get("energy_state")

    print("")
    print("SYSTEM STATE")
    print("--------------------------------------------------")
    print("Ecosystem:", ecosystem)
    print("Energy state:", energy)

    print("")
    print("RISK MONITORING")
    print("--------------------------------------------------")

    transition_probability = None

    if transition_state:
        transition_probability = transition_state.get("transition_probability",0)
        print("Transition probability:",round(transition_probability,3))

    print("Transition risk:", transition_risk)

    print("")
    print("MACRO CONTEXT")
    print("--------------------------------------------------")

    if macro_climate:
        print("Macro climate:",macro_climate.get("macro_climate"))

    if liquidity_wave:
        print("Liquidity wave:",liquidity_wave.get("wave_state"))

    print("")
    print("FORWARD EXPECTATION")
    print("--------------------------------------------------")

    exp_3m = 0
    exp_6m = 0
    exp_12m = 0

    if macro_memory:

        expectations = macro_memory.get("conditioned_pressure_expectation",{})

        exp_3m = expectations.get("3",0)
        exp_6m = expectations.get("6",0)
        exp_12m = expectations.get("12",0)

        print("3m pressure expectation:",round(exp_3m,4))
        print("6m pressure expectation:",round(exp_6m,4))
        print("12m pressure expectation:",round(exp_12m,4))

    print("")
    print("STRATEGIC POSTURE")
    print("--------------------------------------------------")

    if ecosystem == "Liquidity Expansion Ecosystem" and transition_risk == "Low Transition Risk":

        posture = "Expansion Opportunity"

    elif transition_risk == "High Transition Risk":

        posture = "High Volatility Environment"

    else:

        posture = "Neutral Observation"

    print("Recommended posture:", posture)

    dashboard = {

        "ecosystem": ecosystem,
        "energy_state": energy,
        "transition_probability": transition_probability,
        "transition_risk": transition_risk,
        "macro_climate": macro_climate,
        "liquidity_wave": liquidity_wave,
        "3m_expectation": exp_3m,
        "6m_expectation": exp_6m,
        "12m_expectation": exp_12m,
        "strategic_posture": posture

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(dashboard,f)

    print("")
    print("Dashboard saved:")
    print(OUTPUT_FILE)

    print("==================================================")


if __name__ == "__main__":
    main()
