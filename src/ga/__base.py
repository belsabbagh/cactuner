import random
from typing import Callable
import warnings

from src.ga.individual import Individual


class GeneticAlgorithm(object):
    """Genetic Algorithm class."""

    _fitness: Callable[[Individual], float] = None
    _crossover: Callable[[list[Individual]], list[Individual]] = None
    _mutate: Callable[[Individual], Individual] = None
    _select: Callable[[list[Individual]], list[Individual]] = None

    def __init__(self, **kwargs):
        """Initialize the Genetic Algorithm class."""
        self._fitness = kwargs.get("fitness")
        self._crossover = kwargs.get("crossover")
        self._mutate = kwargs.get("mutate")
        self._select = kwargs.get("select")

    @classmethod
    def create(
        cls,
        validate: callable = None,
        fitness: Callable[[Individual, any], float] = None,
        crossover=None,
        mutate=None,
        select=None,
    ):
        """Create a Genetic Algorithm object."""
        if not issubclass(cls, GeneticAlgorithm):
            raise TypeError(f"{cls} is not a subclass of GeneticAlgorithm.")
        return cls(**cls.build_attributes(validate, fitness, crossover, mutate, select))

    @staticmethod
    def build_attributes(
        validate: callable,
        fitness: Callable[[Individual, any], float],
        crossover,
        mutate,
        select,
    ):
        """Initialize the default attributes."""
        if fitness is None:
            raise ValueError("No fitness function was defined.")
        return {
            "validate": validate if validate is not None else lambda x: True,
            "fitness": fitness,
            "crossover": crossover if crossover is not None else lambda x, y: x,
            "mutate": mutate if mutate is not None else lambda x: x,
            "select": select
            if select is not None
            else lambda x: x[: int(len(x) * 0.05)],
        }

    def get_fitness(self):
        return self._fitness

    def get_crossover(self):
        return self._crossover

    def get_mutate(self):
        return self._mutate

    def get_select(self):
        return self._select

    def _check_params(self, population, generations, zero_best, log, reverse):
        if zero_best and reverse:
            raise ValueError("Cannot set zero_best and reverse to True.")

    def run(
        self,
        population: list[Individual],
        generations,
        zero_best: bool = False,
        max_fitness: bool = False,
        verbose: bool = False,
    ):
        self._check_params(population, generations, zero_best, verbose, max_fitness)
        return self._run(
            population, generations, self._fitness, self._new_pool, max_fitness, verbose
        )

    @staticmethod
    def _run(
        population: list[Individual],
        generations,
        fitness,
        create_new_pool,
        max_fitness: bool = False,
        verbose: bool = False,
    ):
        pool = population
        """Run the Genetic Algorithm."""
        for gen_i in range(1, generations + 1):
            if pool == []:
                raise RuntimeError("There were no survivors.")
            pool = sorted(
                [(i, fitness(i)) for i in pool], key=lambda x: x[1], reverse=max_fitness
            )
            best_ind, best_score = pool[0]
            if verbose:
                print(
                    GeneticAlgorithm._log_msg(
                        gen_i, best_ind.get_solution(), best_score, len(pool)
                    )
                )
            pool = create_new_pool(pool)
        if fitness(pool[0]) == 0 and max_fitness:
            warnings.warn("No solution was found.")
        return pool

    def _reproduce(self, parents: list[Individual]):
        """Create a new generation of individuals."""
        new_gen = []
        for i in range(1, len(parents)):
            kids = self._crossover(parents[i], parents[i - 1])
            new_gen.extend([self._mutate(ind) for ind in kids])
        return new_gen

    @staticmethod
    def _log_msg(generation, best: Individual, fitness_score, pool_size):
        """Generate a log message."""
        return f"Gen {generation: >6}: Best: {best} Fitness: {round(fitness_score, 5): <10} Pool: {pool_size}"

    @staticmethod
    def _get_ratio(population: list[Individual], ratio: float):
        """Return the fittest individual in the population."""
        return population[: int(len(population) * ratio)]

    def _new_pool(self, pool: list[tuple[Individual, float]]):
        """Create a new pool of individuals."""
        individuals = [i for i, _ in pool]
        return self._reproduce(self._select(pool)) + individuals[:5]
