# region_map.py
# DNA Geográfico do Planeta Bitcoin
# Cada região representa um campo de força económico, psicológico e cultural
# que influencia como o capital se move e como o mercado "soa".

REGIONS = {
    "north_america": {
        "label": "North America",
        "centers": ["USA", "Canada"],
        "archetype": "Institutional Capital",
        "volatility_bias": 0.6,
        "volume_bias": 1.3,
        "confidence_bias": 1.2,
        "musical_style": "Cinematic / Orchestral / Wall Street",
        "instruments": ["Strings", "Brass", "Grand Piano"],
        "tempo_bias": 0.9
    },

    "europe": {
        "label": "Europe",
        "centers": ["EU", "UK", "Switzerland"],
        "archetype": "Regulated Capital",
        "volatility_bias": 0.4,
        "volume_bias": 0.9,
        "confidence_bias": 1.1,
        "musical_style": "Classical / Minimalist / Chamber",
        "instruments": ["Piano", "Cello", "Clarinet"],
        "tempo_bias": 0.8
    },

    "east_asia": {
        "label": "East Asia",
        "centers": ["China", "Korea", "Japan", "Hong Kong"],
        "archetype": "Liquidity Engines",
        "volatility_bias": 1.3,
        "volume_bias": 1.4,
        "confidence_bias": 0.9,
        "musical_style": "High-Energy / Percussive / Digital",
        "instruments": ["Taiko", "Synth Leads", "Arpeggiators"],
        "tempo_bias": 1.3
    },

    "crypto_native": {
        "label": "Crypto Native",
        "centers": ["DeFi", "Whales", "DEXs", "On-chain"],
        "archetype": "Speculative Intelligence",
        "volatility_bias": 1.6,
        "volume_bias": 1.5,
        "confidence_bias": 0.7,
        "musical_style": "Experimental / Modular / Glitch",
        "instruments": ["Modular Synth", "Granular FX", "Digital Bass"],
        "tempo_bias": 1.4
    },

    "emerging_markets": {
        "label": "Emerging Markets",
        "centers": ["LATAM", "Africa", "Middle East", "South Asia"],
        "archetype": "Survival Capital",
        "volatility_bias": 1.1,
        "volume_bias": 0.8,
        "confidence_bias": 1.4,
        "musical_style": "Organic / Rhythmic / Tribal",
        "instruments": ["Drums", "Flutes", "Acoustic Strings"],
        "tempo_bias": 1.1
    }
}

# Regiões por fuso horário aproximado (para inferir dominância por hora do dia)
TIMEZONE_DOMINANCE = {
    "00-08": "east_asia",
    "08-16": "europe",
    "16-24": "north_america"
}
