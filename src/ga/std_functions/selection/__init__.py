import numpy as np
from src.ga.individual import Individual


def roulette_selection(
    population: list[tuple[Individual, float]], proportion
) -> list[Individual]:
    """
    Selects individuals based on their fitness value.
    """
    if proportion > 1 or proportion < 0:
        raise ValueError("Proportion must be between 0 and 1")
    total_fitness = sum([x[1] for x in population])
    individuals = [x[0] for x in population]
    if total_fitness == 0:
        return individuals[: int(len(individuals) * proportion)]
    probabilities = [x[1] / total_fitness for x in population]
    random_number = np.random.random()
    cumulative_probability = 0
    for i, probability in enumerate(probabilities):
        cumulative_probability += probability
        if cumulative_probability >= random_number:
            return individuals[: i + 1] + individuals[i + 1 : int(len(individuals) * proportion)]
