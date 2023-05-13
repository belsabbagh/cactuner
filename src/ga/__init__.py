"""
Genetic Algorithm
"""
from .__base import GeneticAlgorithm
from .individual import Individual, NumberIndividual


GeneticAlgorithm = GeneticAlgorithm


class NumberGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def mutate(x):
        return NumberIndividual.fmt_mutation(x)
