from src.ga.individual import Individual


def run(
    population: list[Individual],
    generations,
    fitness,
    create_new_pool,
    max_fitness: bool = False,
    verbose: bool = False,
):
    """Run the genetic algorithm.

    Args:
        population (list[Individual]): The initial population.
        generations (int): The number of generations to run.
        fitness (Callable[[Individual, any], float]): The fitness function.
        create_new_pool (Callable[[list[Individual], int], list[Individual]]):
            The function to create a new pool.
        max_fitness (bool, optional): Whether to maximize the fitness function.
            Defaults to False.
        verbose (bool, optional): Whether to print the progress. Defaults to False.

    Returns:
        list[Individual]: The final population.
    """
    pass


def iteration(
    index: int,
    population: list[Individual],
    fitness,
    select,
    crossover,
    mutate,
    elitism_ratio: float,
    max_fitness: bool = False,
    verbose: bool = False,
):
    """Run one iteration of the genetic algorithm.

    Args:
        population (list[Individual]): The initial population.
        fitness (Callable[[Individual, any], float]): The fitness function.
        create_new_pool (Callable[[list[Individual], int], list[Individual]]):
            The function to create a new pool.
        max_fitness (bool, optional): Whether to maximize the fitness function.
            Defaults to False.
        verbose (bool, optional): Whether to print the progress. Defaults to False.

    Returns:
        list[Individual]: The new population.
    """
    pool = population
    pool = sorted(
        [(i, fitness(i)) for i in pool], key=lambda x: x[1], reverse=max_fitness
    )
    best_ind, best_score = pool[0]
    if verbose:
        _log_msg(index, best_ind.get_solution(), best_score, len(pool))
    return _create_new_pool(pool, select, crossover, mutate, elitism_ratio)


def _log_msg(generation, best: Individual, fitness_score, pool_size):
    """Generate a log message."""
    return f"Gen {generation: >6}: Best: {best} Fitness: {round(fitness_score, 5): <10} Pool: {pool_size}"


def _create_new_pool(
    population: list[tuple[Individual, float]], select, crossover, mutate, elitism_ratio
):
    """Create a new generation of individuals."""
    parents = select(population)
    new_gen = []
    for i in range(1, len(parents), 2):
        kids = crossover(parents[i], parents[i - 1])
        new_gen.extend([mutate(ind) for ind in kids])
    return new_gen + _get_ratio([i for i, _ in population], elitism_ratio)


def _get_ratio(population: list[Individual], ratio: float):
    """Return the fittest individual in the population."""
    return population[: int(len(population) * ratio)]
