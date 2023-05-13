from src.ga import NumberGeneticAlgorithm
from src.ga.individual import NumberIndividual


if __name__ == '__main__':
    ga = NumberGeneticAlgorithm(
        fitness=lambda x: abs(25 - float(x)*float(x)),
        crossover=lambda x, y: x + y,
        mutate=lambda x: NumberIndividual.mutate(x),
        select=lambda x: x[:int(len(x)*0.05)],
    )
    population = NumberIndividual.random_population(8, list(range(30)))
    res = ga.run(population, 200, debug=True)
    print(f"Answer: {float(res[0])}")