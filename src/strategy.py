import copy
from enum import IntEnum
from string import punctuation
from typing import Callable, Dict, List, Set, Tuple
from src.evolver import Evolver
from src.fitness import MSE, check_words_in_dict_ratio, letters_freq_ratio
from src.decoder import Decoder
from src.sample import Sample


class GeneticAlgorithmType(IntEnum):
    REGULAR = 0
    DARWIN = 1
    LAMARK = 2

    @staticmethod
    def get_strategy(strategy: int, dictionary: Set[str], enc: str, enc_letters: List[str], single_let_freq: Dict[str, float]):
        if strategy == 1:
            return DarwinStrategy(dictionary, enc, enc_letters, single_let_freq)
        if strategy == 2:
            return LamarkStrategy(dictionary, enc, enc_letters, single_let_freq)
        return RegularStrategy(dictionary, enc, enc_letters, single_let_freq)


class BaseStrategy:
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], single_let_freq: Dict[str, float]) -> None:
        self.__enc = enc
        self.__dictionary = dictionary
        self.__single_let_freq = single_let_freq
        self.__evolver: Evolver = Evolver(enc_letters)

    def decode(self, samples: List[Sample]) -> Tuple[List[str], List[List[str]]]:
        dec = [Decoder.decode_words(self.__enc, s.dec_map_int).strip().translate(str.maketrans('', '', f'{punctuation}\n\r')) for s in samples]
        dec_words = [d.split(' ') for d in dec]
        return dec, dec_words


    def fitness(self, samples: List[Sample]) -> Tuple[int, List[float]]:
        decs, dec_words = self.decode(samples)
        fitness_scores = [check_words_in_dict_ratio(dec, self.__dictionary) for dec in dec_words]
        # freq_measure = [letters_freq_ratio(dec, self.__single_let_freq, MSE) for dec in decs]
        return len(dec_words), fitness_scores
    

    def optimize(self, samples: List[Sample], fitness_scores: List[float]) -> List[Sample]:
        optimized: List[Sample] = list()

        for s, f in zip(samples, fitness_scores):
            new_fitness = 0
            new_sample = s
            temp: Sample = copy.deepcopy(s)
            for _ in range(50):
                mutation, c1, c2 = self.__evolver.mutate(temp.dec_map)
                new_fitness = self.fitness([Sample(mutation)])[1][0]

                if new_fitness == 1:
                    break
                
                temp.swap(c1, c2)
            
            # Accept mutation only if it is better
            if new_fitness >= f:
                new_sample = temp
            
            optimized.append(new_sample)
        
        return optimized


class RegularStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], single_let_freq: Dict[str, float]) -> None:
        super().__init__(dictionary, enc, enc_letters, single_let_freq)

    def activate(self, step_func: Callable[[Tuple[List[Sample], List[float]]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        return step_func(samples, fitness_scores)


class DarwinStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], single_let_freq: Dict[str, float]) -> None:
        super().__init__(dictionary, enc, enc_letters, single_let_freq)

    def activate(self, step_func: Callable[[Tuple[List[Sample], List[float]]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        optimized_samples = self.optimize(samples, fitness_scores)
        optimized_fitness = self.fitness(optimized_samples)[1]
        samples, fitness_scores = step_func(samples, optimized_fitness)
        return samples, fitness_scores


class LamarkStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], single_let_freq: Dict[str, float]) -> None:
        super().__init__(dictionary, enc, enc_letters, single_let_freq)

    def activate(self, step_func: Callable[[Tuple[List[Sample], List[float]]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        optimized_samples = self.optimize(samples, fitness_scores)
        optimized_fitness = self.fitness(optimized_samples)[1]
        samples, fitness_scores = step_func(optimized_samples, optimized_fitness)
        return samples, fitness_scores
