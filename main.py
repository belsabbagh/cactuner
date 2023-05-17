import numpy as np
from src.ga import CACGeneticAlgorithm
from src.ga.individual import CACIndividual


if __name__ == "__main__":
    img = np.random.randint(0, 2, size=(12, 12))
    ga = CACGeneticAlgorithm(
        img,
        crossover=lambda x, y: x + y,
        mutate=lambda x: CACIndividual.mutate(x),
        select=lambda x: x[: int(len(x) * 0.2)],
    )
    population = CACIndividual.random_population(30, list(range(1, 13)))
    res = ga.run(population, 30, verbose=True)
    print(f"Answer: {res[0].to_list()}")
