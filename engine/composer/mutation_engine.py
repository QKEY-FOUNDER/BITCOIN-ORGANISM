import copy
import random


# --------------------------------------------------
# Mutation Decision
# --------------------------------------------------

def decide_mutation_level(similarity_score):

    if similarity_score > 0.85:
        return "micro"

    elif similarity_score > 0.5:
        return "moderate"

    else:
        return "new"


# --------------------------------------------------
# Micro Mutation
# --------------------------------------------------

def micro_mutation(snapshot):

    mutated = copy.deepcopy(snapshot)

    # Pequena variação na tensão
    if "harmony" in mutated:
        mutated["harmony"]["tension"] *= random.uniform(0.98, 1.02)

    # Pequena variação na densidade
    if "profile" in mutated:
        mutated["profile"]["density"] *= random.uniform(0.97, 1.03)

    return mutated


# --------------------------------------------------
# Moderate Mutation
# --------------------------------------------------

def moderate_mutation(snapshot):

    mutated = copy.deepcopy(snapshot)

    if "harmony" in mutated:
        mutated["harmony"]["tension"] *= random.uniform(0.9, 1.1)

    if "profile" in mutated:
        mutated["profile"]["tension_base"] *= random.uniform(0.9, 1.1)

    if "risk_score" in mutated:
        mutated["risk_score"] *= random.uniform(0.9, 1.1)

    return mutated


# --------------------------------------------------
# New Identity
# --------------------------------------------------

def new_identity(snapshot):

    mutated = copy.deepcopy(snapshot)

    # Reinicializa valores chave
    mutated["risk_score"] = random.uniform(0.2, 0.8)

    if "profile" in mutated:
        mutated["profile"]["tension_base"] = random.uniform(0.3, 0.9)
        mutated["profile"]["density"] = random.uniform(0.3, 0.8)

    if "harmony" in mutated:
        mutated["harmony"]["tension"] = random.uniform(0.3, 1.0)

    return mutated


# --------------------------------------------------
# Main Mutation Engine
# --------------------------------------------------

def mutate_snapshot(snapshot, similarity_score):

    level = decide_mutation_level(similarity_score)

    if level == "micro":
        return micro_mutation(snapshot)

    elif level == "moderate":
        return moderate_mutation(snapshot)

    else:
        return new_identity(snapshot)
