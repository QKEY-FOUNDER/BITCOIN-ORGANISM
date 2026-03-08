def evaluate_health(stress, volume, geo_vector):
    """
    Avalia estado fisiológico do organismo Bitcoin.

    stress → normalizado 0–1 (volatilidade intradiária)
    volume → volume bruto
    geo_vector → distribuição geopolítica ponderada
    """

    geo_stability = geo_vector.get("stability", 0.5)

    # Stress elevado + baixa estabilidade = infeção sistémica
    if stress > 0.75 and geo_stability < 0.4:
        return "INFECTED"

    # Stress moderado ou volume anómalo
    if stress > 0.55:
        return "STRESSED"

    # Estado basal saudável
    return "HEALTHY"
