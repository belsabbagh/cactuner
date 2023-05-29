from src.ga.individual import Individual


class Population:
    ppl = list[Individual] = None

    def __init__(self, population: list[Individual]) -> None:
        self.ppl = population

    def __len__(self):
        return len(self.ppl)

    def fitness(
        self, fitness: callable, descending=False
    ) -> list[tuple[Individual, float]]:
        """
        Gets the fitness for each individual.
        Creates a list of tuples of the individual and their fitness value.
        Returns the list sorted by fitness value.
        """
        return sorted(
            [(x, fitness(x)) for x in self.ppl], key=lambda x: x[1], reverse=descending
        )

    def select(self, select: callable) -> list[Individual]:
        """Applies the given selection function on the population."""
        return select(self.ppl)

    def evolve(
        self, select: callable, crossover: callable, mutate: callable
    ) -> list[Individual]:
        """
        Calculates fitness.
        Selects.
        Crossovers.
        Mutates.
        Returns the new population.
        """
        raise NotImplementedError("evolve() is not implemented")

    def get_best(self, fitness: callable, descending=False) -> tuple[Individual, float]:
        """Returns the best individual and their fitness value."""
        raise NotImplementedError("get_best() is not implemented")
