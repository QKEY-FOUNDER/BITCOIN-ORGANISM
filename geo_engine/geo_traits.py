# geo_traits.py
# DNA acústico da Terra
# Traduz dominância geográfica em comportamento musical

GEO_TRAITS = {
    "north_america": {
        "bpm": 110,
        "rhythm_density": 0.7,
        "harmonic_aggression": 0.6,
        "brightness": 0.8,
        "stability": 0.7
    },

    "europe": {
        "bpm": 90,
        "rhythm_density": 0.5,
        "harmonic_aggression": 0.4,
        "brightness": 0.6,
        "stability": 0.9
    },

    "east_asia": {
        "bpm": 125,
        "rhythm_density": 0.85,
        "harmonic_aggression": 0.8,
        "brightness": 0.9,
        "stability": 0.6
    },

    "crypto_native": {
        "bpm": 135,
        "rhythm_density": 1.0,
        "harmonic_aggression": 1.0,
        "brightness": 0.7,
        "stability": 0.3
    },

    "emerging_markets": {
        "bpm": 80,
        "rhythm_density": 0.6,
        "harmonic_aggression": 0.5,
        "brightness": 0.5,
        "stability": 0.5
    }
}

def combine_geo_traits(geo_vector):
    """
    geo_vector = { region: dominance }
    returns a single acoustic state for the month
    """
    result = {
        "bpm": 0,
        "rhythm_density": 0,
        "harmonic_aggression": 0,
        "brightness": 0,
        "stability": 0
    }

    for region, weight in geo_vector.items():
        traits = GEO_TRAITS.get(region)
        if not traits:
            continue

        for key in result:
            result[key] += traits[key] * weight

    return result
