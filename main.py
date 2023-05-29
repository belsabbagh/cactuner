import numpy as np
from src.ga import CACGeneticAlgorithm
from src.ga.individual import CACIndividual
from src.ga.std_functions.selection import roulette_selection


SIZE = 512


if __name__ == "__main__":
    img = np.random.randint(0, 2, size=(SIZE, SIZE))
    ga = CACGeneticAlgorithm(
        img,
        crossover=lambda x, y: x + y,
        mutate=lambda x: CACIndividual.mutate(x),
        select=lambda x: roulette_selection(x, 0.5),
    )
    population = CACIndividual.random_population(150, list(range(1, SIZE + 1)))
    res = ga.run(population, 50, verbose=True)
    print(f"Answer: {res[0].to_list()}")
