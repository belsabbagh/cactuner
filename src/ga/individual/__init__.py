"""
This module contains the Individual class.
"""


import random


def _create_child_chromosome(c1, c2):
    child1, child2 = [], []
    for gp1, gp2 in zip(c1, c2):
        prob = random.random()
        if prob < 0.5:
            child1.append(gp1)
            child2.append(gp2)
        else:
            child1.append(gp2)
            child2.append(gp1)
    return child1, child2


class Individual(object):
    """Individual class."""

    def __init__(self, chromosome: list = None):
        if chromosome is None:
            chromosome = []
        self._chromosome = chromosome
        """Initialize the Individual class."""

    def get_chromosome(self):
        """Return the chromosome of the individual."""
        return self._chromosome

    @classmethod
    def random_population(cls, size: int, target_size, genes):
        """Create a random population of individuals."""
        return [
            cls([random.choice(genes) for _ in range(target_size)]) for _ in range(size)
        ]

    @classmethod
    def mate(cls, par1, par2):
        """
        Perform mating and produce new offspring
        """
        c1, c2 = _create_child_chromosome(par1.get_chromosome(), par2.get_chromosome())
        return cls(c1), cls(c2)

    def __add__(self, other):
        return self.__class__.mate(self, other)

    def add_mutations(self, genes):
        """Add mutations to the individual."""
        self._chromosome[random.randint(0, len(self._chromosome) - 1)] = random.choice(
            genes
        )
        return self

    @staticmethod
    def mutate(x):
        index = random.randint(0, len(x.get_chromosome()) - 1)
        x.get_chromosome()[index] = 1 - x.get_chromosome()[index]
        return x


def bin_str(n: float | int) -> str:
    return f"{int(str(round(n, 2)).replace('.', '')):b}"


class NumberChromosome:
    def __init__(self, chromosome: float | int | list = None):
        self.chromosome = (
            [int(i) for i in bin_str(chromosome)]
            if self._is_number(chromosome)
            else chromosome
        )

    @staticmethod
    def _is_number(n) -> bool:
        return type(n) is int or type(n) is float

    @staticmethod
    def to_string(s):
        return "".join([str(i) for i in s])

    def __int__(self):
        return int(self.to_string(self.chromosome), 2)


class CACIndividual:
    def __init__(self, window_size, as_is=False):
        self.chromosome = (
            [[int(j) for j in bin_str((i))] for i in window_size]
            if not as_is
            else window_size
        )

    def __add__(self, other):
        return self.__class__.mate(self, other)

    @classmethod
    def mate(cls, par1, par2):
        c1, c2 = _create_child_chromosome(par1.get_chromosome(), par2.get_chromosome())
        return cls(c1, as_is=True), cls(c2, as_is=True)

    @classmethod
    def random_population(cls, size: int, genes):
        """Create a random population of individuals."""
        return [
            cls(i)
            for i in [(random.choice(genes), random.choice(genes)) for _ in range(size)]
        ]

    def get_chromosome(self):
        return self.chromosome

    @staticmethod
    def mutate(x):
        for i in range(len(x.get_chromosome())):
            index = random.randint(0, len(x.get_chromosome()[i]) - 1)
            x.get_chromosome()[i][index] = 1 - x.get_chromosome()[i][index]
        return x

    def to_list(self):
        return [int(NumberChromosome.to_string(i), base=2) for i in self.get_chromosome()]

    def get_solution(self):
        return self.to_list()