# --------------------------------------------------
# Phase Engine
# Bitcoin Organism — Market Regime Classification
# --------------------------------------------------


# --------------------------------------------------
# Configuração fisiológica
# --------------------------------------------------

SHOCK_ACCEL_THRESHOLD = 1.0        # aceleração extrema que dispara Shock
SHOCK_COOLDOWN_MONTHS = 2          # meses mínimos antes de poder sair de Shock
SHOCK_TENSION_RELEASE = 0.55       # tensão abaixo da qual o organismo pode recuperar
SHOCK_TENSION_TRIGGER = 0.60       # tensão mínima para permitir Shock


# --------------------------------------------------
# Classificação base (sem memória)
# --------------------------------------------------

def base_phase_classification(bundle):

    values = bundle["values"]

    tension = values.get("structural_tension", 0)
    vol = values.get("volatility_resonance", 0)

    if tension > 0.7:
        return "Instability"

    if tension < 0.35 and abs(vol) < 0.2:
        return "Equilibrium"

    return "Transition"


# --------------------------------------------------
# Classificador principal
# Inclui:
# 1) Override Shock
# 2) Cooldown biológico
# 3) Inércia de fase
# --------------------------------------------------

def classify_market_phase(bundle, previous_phase=None, previous_count=0):

    values = bundle["values"]
    acceleration = bundle["acceleration"]

    tension = values.get("structural_tension", 0)
    acc = acceleration.get("volatility_acceleration", 0)

    # --------------------------------------------------
    # 1. Override Shock (evento extremo real)
    # Shock só ocorre se houver:
    # aceleração extrema + tensão elevada
    # --------------------------------------------------

    if abs(acc) > SHOCK_ACCEL_THRESHOLD and tension > SHOCK_TENSION_TRIGGER:
        return "Shock", 1

    candidate = base_phase_classification(bundle)

    # --------------------------------------------------
    # Primeira execução
    # --------------------------------------------------

    if previous_phase is None:
        return candidate, 1

    # --------------------------------------------------
    # 2. Cooldown biológico do Shock
    # --------------------------------------------------

    if previous_phase == "Shock":

        # organismo ainda em trauma mínimo
        if previous_count < SHOCK_COOLDOWN_MONTHS:
            return "Shock", previous_count + 1

        # tensão ainda elevada → continua em Shock
        if tension > SHOCK_TENSION_RELEASE:
            return "Shock", previous_count + 1

        # tensão caiu → organismo começa recuperação
        return candidate, 1

    # --------------------------------------------------
    # 3. Inércia natural de fase
    # evita mudanças demasiado rápidas
    # --------------------------------------------------

    if candidate == previous_phase:
        return candidate, previous_count + 1

    # permitir mudança após 2 ciclos
    if previous_count >= 2:
        return candidate, 1

    # caso contrário mantém fase anterior
    return previous_phase, previous_count + 1
