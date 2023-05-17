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
        raise NotImplementedError("fitness() is not implemented")

    def select(self, select: callable) -> list[Individual]:
        """Applies the given selection function on the population."""
        raise NotImplementedError("select() is not implemented")

    def evolve(self, crossover: callable, mutate: callable) -> list[Individual]:
        """
        Calculates fitness.
        Selects.
        Crossovers.
        Mutates.
        Returns the new population.
        """
        raise NotImplementedError("evolve() is not implemented")
