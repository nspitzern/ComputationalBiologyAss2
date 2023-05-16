from typing import List
from math import floor
from random import sample

from src.generator import Sample


class Selector:
    @staticmethod
    def select_elite(samples, fitness_scores, percentile: float) -> List[Sample]:
        """

        :param samples:
        :param fitness_scores:
        :param percentile: Which percentile to keep
        :return:
        """
        ratio = floor(len(fitness_scores) - percentile * len(fitness_scores))  # how many samples to return

        # sort the
        samples, fitness_scores = zip(*sorted(zip(samples, fitness_scores), key=lambda x: x[1]))
        return samples[len(samples) - ratio:]

    @staticmethod
    def choose_2_random(arr: List[str]):
        return sample(range(len(arr)), 2)
