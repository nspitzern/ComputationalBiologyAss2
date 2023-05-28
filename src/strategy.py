import copy
from enum import IntEnum
from string import punctuation
from typing import Callable, Dict, List, Set, Tuple
from src.evolver import Evolver
from src.fitness import MSE, NMSE, abs_diff, minus_freq_diff, check_words_in_dict_ratio, letters_freq_ratio, word_correctness_by_len
from src.decoder import Decoder
from src.sample import Sample


class GeneticAlgorithmType(IntEnum):
    REGULAR = 0
    DARWIN = 1
    LAMARK = 2

    @staticmethod
    def get_strategy(strategy: int, dictionary: Set[str], enc: str, enc_letters: List[str], unigram_freq: Dict[str, float], bigram_freq: Dict[str, float]):
        if strategy == 1:
            return DarwinStrategy(dictionary, enc, enc_letters, unigram_freq, bigram_freq)
        if strategy == 2:
            return LamarkStrategy(dictionary, enc, enc_letters, unigram_freq, bigram_freq)
        return RegularStrategy(dictionary, enc, enc_letters, unigram_freq, bigram_freq)

    @staticmethod
    def map_to_str(strategy: int) -> str:
        m = {
            GeneticAlgorithmType.REGULAR: 'REGULAR',
            GeneticAlgorithmType.DARWIN: 'DARWIN',
            GeneticAlgorithmType.LAMARK: 'LAMARK',
        }

        return m.get(strategy, '')


class BaseStrategy:
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], unigram_freq: Dict[str, float], bigram_freq: Dict[str, float]) -> None:
        self.__enc = enc
        self.__dictionary = dictionary
        self.unigram_freq = unigram_freq
        self.bigram_freq = bigram_freq
        self.__evolver: Evolver = Evolver(enc_letters)
        self.fitness_calls = 0

    def decode(self, samples: List[Sample]) -> Tuple[List[str], List[List[str]]]:
        dec = [Decoder.decode_words(self.__enc, s.dec_map_int).strip().translate(str.maketrans('', '', f'{punctuation}\n\r')) for s in samples]
        dec_words = [d.split(' ') for d in dec]
        return dec, dec_words

    def fitness(self, samples: List[Sample]) -> List[float]:
        self.fitness_calls += len(samples)
        decs, dec_words = self.decode(samples)
        words_in_dict_measure = [check_words_in_dict_ratio(dec, self.__dictionary) for dec in dec_words]
        # word_correctness_measure = [word_correctness_by_len(dec, self.__dictionary) for dec in dec_words]
        minus_diff_freq_measure = [letters_freq_ratio(dec, self.unigram_freq, self.bigram_freq, minus_freq_diff) for dec in decs]

        # fitness_scores = words_in_dict_measure
        # fitness_scores = [(a * 8 + b + c) / 10 for a, b, c in zip(words_in_dict_measure, word_correctness_measure, minus_diff_freq_measure)]
        fitness_scores = [(a * 9 + b) / 10 for a, b in zip(words_in_dict_measure, minus_diff_freq_measure)]

        return fitness_scores
    

    def optimize(self, samples: List[Sample], fitness_scores: List[float]) -> List[Sample]:
        optimized: List[Sample] = list()
        prev_fitness = 0

        for s, f in zip(samples, fitness_scores):
            new_fitness = 0
            new_sample = s
            temp: Sample = copy.deepcopy(s)
            for _ in range(10):
                mutation, swaps = self.__evolver.swap_mutation(temp.dec_map)
                new_fitness = self.fitness([Sample(mutation)])[0]

                if new_fitness == 1:
                    break
                
                temp.swap(swaps)
            
            # Accept mutation only if it is better
            if new_fitness >= f and new_fitness > prev_fitness:
                new_sample = temp
                prev_fitness = new_fitness
            
            optimized.append(new_sample)
        
        return optimized


class RegularStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], unigram_freq: Dict[str, float], bigram_freq: Dict[str, float]) -> None:
        super().__init__(dictionary, enc, enc_letters, unigram_freq, bigram_freq)

    def activate(self, step_func: Callable[[List[Sample], List[float]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        return step_func(samples, fitness_scores)


class DarwinStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], unigram_freq: Dict[str, float], bigram_freq: Dict[str, float]) -> None:
        super().__init__(dictionary, enc, enc_letters, unigram_freq, bigram_freq)

    def activate(self, step_func: Callable[[List[Sample], List[float]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        optimized_samples = self.optimize(samples, fitness_scores)
        optimized_fitness = self.fitness(optimized_samples)
        samples, fitness_scores = step_func(samples, optimized_fitness)
        return samples, fitness_scores


class LamarkStrategy(BaseStrategy):
    def __init__(self, dictionary: Set[str], enc: str, enc_letters: List[str], unigram_freq: Dict[str, float], bigram_freq: Dict[str, float]) -> None:
        super().__init__(dictionary, enc, enc_letters, unigram_freq, bigram_freq)

    def activate(self, step_func: Callable[[List[Sample], List[float]], Tuple[List[Sample], List[float]]], samples: List[Sample], fitness_scores: List[float]) -> Tuple[List[Sample], List[float]]:
        optimized_samples = self.optimize(samples, fitness_scores)
        optimized_fitness = self.fitness(optimized_samples)
        samples, fitness_scores = step_func(optimized_samples, optimized_fitness)
        return samples, fitness_scores
