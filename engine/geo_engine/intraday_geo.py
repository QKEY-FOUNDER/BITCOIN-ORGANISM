def compute_intraday_geo_vector():
    """
    Simulação básica de atividade geopolítica por hora.
    Retorna dicionário {hora: {região: peso}}
    """

    profile = {}

    for hour in range(24):
        if 13 <= hour <= 20:
            profile[hour] = {"north_america": 1.0}
        elif 7 <= hour <= 12:
            profile[hour] = {"europe": 0.9}
        elif 0 <= hour <= 6:
            profile[hour] = {"east_asia": 0.8}
        else:
            profile[hour] = {"global": 0.6}

    return profile
