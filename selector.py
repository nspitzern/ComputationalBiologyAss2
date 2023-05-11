from typing import List
from math import floor
from generator import Sample


class Selector:
    def __init__(self):
        pass

    def select_elite(self, samples, fitness_scores, percentile: float) -> List[Sample]:
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
