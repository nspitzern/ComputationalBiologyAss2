from enum import IntEnum
from string import punctuation
from typing import Callable, List, Set, Tuple
from src.fitness import check_words_in_dict_ratio
from src.decoder import Decoder
from src.sample import Sample


class GeneticAlgorithmType(IntEnum):
    REGULAR = 0
    DARWIN = 1
    LAMARK = 2

    @staticmethod
    def get_strategy(strategy: int, dictionary: Set[str], enc: str):
        if strategy == 1:
            return DarwinStrategy(dictionary, enc)
        if strategy == 1:
            return LamarkStrategy(dictionary, enc)
        return RegularStrategy(dictionary, enc)


class BaseStrategy:
    def __init__(self, dictionary: Set[str], enc: str) -> None:
        self.__enc = enc
        self.__dictionary = dictionary

    def decode(self, samples: List[Sample]) -> Tuple[List[str], List[List[str]]]:
        dec = [Decoder.decode_words(self.__enc, s.dec_map_int).strip().translate(str.maketrans('', '', f'{punctuation}\n\r')) for s in samples]
        dec_words = [d.split(' ') for d in dec]
        return dec, dec_words


    def fitness(self, samples: List[Sample]) -> Tuple[int, List[float]]:
        decs, dec_words = self.decode(samples)
        return len(dec_words), [check_words_in_dict_ratio(dec, self.__dictionary) for dec in dec_words]
    

    def optimize(self, samples: List[Sample]) -> List[Sample]:
        # TODO: implement optimizations
        return samples


class RegularStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str) -> None:
        super().__init__(dictionary, enc)

    def activate(self, step_func: Callable[[Tuple[List[Sample], List[float]]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        return step_func(samples, fitness_scores)


class DarwinStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str) -> None:
        super().__init__(dictionary, enc)

    def activate(self, step_func: Callable[[Tuple[List[Sample], List[float]]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        optimized_samples = self.optimize(samples)
        optimized_fitness = self.fitness(optimized_samples)[1]
        samples, fitness_scores = step_func(samples, optimized_fitness)
        return samples, fitness_scores


class LamarkStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str) -> None:
        super().__init__(dictionary, enc)

    def activate(self, step_func: Callable[[Tuple[List[Sample], List[float]]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        optimized_samples = self.optimize(samples)
        optimized_fitness = self.fitness(optimized_samples)[1]
        samples, fitness_scores = step_func(optimized_samples, optimized_fitness)
        return samples, fitness_scores
