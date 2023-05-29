from itertools import permutations
from random import randint, sample, uniform

from src.ga.evolution import evolve

from src.cac import CAC


def genetic_algorithm(
    image_array,
    block_sizes,
    delta_error=10**-5,
    least_number_of_generations=5,
    debug=False,
):
    """Genetic Algorithm (Optimization) for CAC"""
    max_CR = {"CR": -1, "block_width": 0, "block_height": 0}
    temp_string = str("# Genetic Algorithm (Optimization):")
    if debug:    
        print(temp_string)
        print("=" * len(temp_string))
    population_size, n_parents, least_number_of_mating_pools, multiplicat = get_params(
        block_sizes
    )
    if debug:
        print_metadata(
            block_sizes,
            multiplicat,
            population_size,
            least_number_of_mating_pools,
            n_parents,
            least_number_of_generations,
            delta_error,
        )
    if debug:
        print("Processing", end="", flush=True)
    i = 10
    generations_counter = 0
    new_populations = init_population(block_sizes, population_size)
    condition = True
    while condition:
        last_max_CR = max_CR.copy()
        generations_counter += 1
        population = [
            (CAC(image_array, width, height), width, height)
            for width, height in new_populations.copy()
        ]
        population.sort(reverse=True)
        max_CR = {
            "CR": population[0][0],
            "block_width": population[0][1],
            "block_height": population[0][2],
        }
        population = evolve(population, population_size, n_parents, block_sizes)
        condition = (generations_counter < least_number_of_generations) or (
            (max_CR["CR"] - last_max_CR["CR"]) > delta_error
        )
        if debug:
            temp_string = "Generation: (" + str(generations_counter) + ")"
            print_iteration(
                temp_string,
                population,
                max_CR,
            )

    if (not debug) and (i < 150 or i % 150 != 0):
        print()
    return max_CR


def print_iteration(
    temp_string,
    population,
    max_CR,
):
    print(temp_string)
    print("-" * len(temp_string))
    print(
        "Sorted Populations with Fitnesses (CR,BlockWidth,BlockHeight): "
        + str(population)
    )
    print("Best Compression Ratio: " + str(max_CR["CR"]))


def pretty_print(i, debug):
    if debug:
        if i < 150 or i % 150 != 0:
            print("*", end="", flush=True)
        else:
            print("\n*", end="", flush=True)
        i = i + 1
    else:
        if i == 10:
            i += 1
        else:
            print(" " * 25 + "-" * 100)


def print_metadata(
    block_sizes,
    multiplicat,
    population_size,
    least_number_of_mating_pools,
    n_parents,
    least_number_of_generations,
    delta_error,
):
    print("Least Number of Generations: " + str(least_number_of_generations))
    print("delta Error of Convergence: " + str(delta_error))
    print(
        "Population Size [3->"
        + str(int(len(block_sizes) * multiplicat))
        + "]: "
        + str(population_size)
    )
    print(
        "Number of Mating Pools ["
        + str(least_number_of_mating_pools)
        + "->"
        + str(population_size)
        + "]: "
        + str(n_parents)
    )
    print("Mutation Percentage {0%,50%,100%}: 50%")


def get_params(block_sizes):
    multiplicat = uniform((3 / len(block_sizes)), 0.1)
    if len(block_sizes) < 30:
        multiplicat = 3 / len(block_sizes)
    if multiplicat <= 1:
        population_size = randint(3, int(len(block_sizes) * multiplicat))
    else:
        population_size = len(block_sizes)
    least_number_of_mating_pools = population_size
    for X in range(population_size):
        if population_size <= (X + len(list(permutations([None] * X, 2)))):
            least_number_of_mating_pools = X
            break
    n_parents = randint(least_number_of_mating_pools, population_size)
    return population_size, n_parents, least_number_of_mating_pools, multiplicat


def init_population(
    block_sizes,
    population_size,
):
    new_populations = []
    random_indexes = sample(range(len(block_sizes)), population_size)
    for i in range(population_size):
        new_populations += [block_sizes[random_indexes[i]]]
    return new_populations