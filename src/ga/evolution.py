from itertools import permutations
from random import randint, sample


def make_mating_pools(population, n_parents):
    """Get the best parent chromosomes from the population"""
    mating_pools = [population[i][1:] for i in range(n_parents)]
    # print("Mating Pools (BlockWidth,BlockHeight):  " + str(mating_pools))
    return mating_pools


def get_possible_offsprings(mating_pools):
    """Get all possible offsprings from the mating pools"""
    return [(X1, Y2) for (X1, _), (_, Y2) in list(permutations(mating_pools, 2))]


def generate_offsprings(possible_offsprings, population_size, n_parents):
    """Generate offsprings from the possible offsprings"""
    offsprings = []
    random_indexes = sample(
        range(len(possible_offsprings)), population_size - n_parents
    )
    for i in range(population_size - n_parents):
        offsprings += [possible_offsprings[random_indexes[i]]]
    # print("Offsprings (BlockWidth,BlockHeight):    " + str(offsprings))
    return offsprings


def mutate_population(offsprings, block_sizes):
    """Mutate offsprings"""
    mutants = offsprings.copy()
    for i in range(len(mutants)):
        index = randint(0, 1)
        temp_mutant = list(mutants[i])
        temp_mutant[index] = block_sizes[randint(0, len(block_sizes) - 1)][index]
        mutants[i] = tuple(temp_mutant)
    # print("Mutants (BlockWidth,BlockHeight):       " + str(mutants))
    return mutants


def evolve(population, population_size, n_parents, block_sizes):
    """Evolve the current population"""
    mating_pools = make_mating_pools(population, n_parents)
    possible_offsprings = get_possible_offsprings(mating_pools)
    offsprings = generate_offsprings(possible_offsprings, population_size, n_parents)
    mutants = mutate_population(offsprings, block_sizes)
    return mating_pools + mutants
