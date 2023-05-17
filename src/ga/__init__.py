"""
Genetic Algorithm
"""
from src.cac import compress, compression_ratio
from .__base import GeneticAlgorithm
from .individual import Individual


GeneticAlgorithm = GeneticAlgorithm


class CACGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self, img, **kwargs):
        self.img = img
        super().__init__(**kwargs)

    def fitness(self, x):
        try:
            for i in x.to_list():
                if i == 0:
                    return 0
            if x.to_list() == [1, 1]:
                return 0
            return compression_ratio(self.img, compress(self.img, x.to_list()))
        except Exception:
            return 0

    def run(
        self,
        population: list[Individual],
        generations,
        verbose: bool = False,
    ):
        return self._run(
            population,
            generations,
            self.fitness,
            self._new_pool,
            max_fitness=True,
            verbose=verbose,
        )
