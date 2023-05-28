from typing import Dict, List, Tuple
from random import randint, shuffle
from copy import deepcopy

from src.generator import is_valid
from src.sample import Sample
from src.selector import Selector


class Evolver:
    def __init__(self, enc_letters: List[str]):
        self.__length = len(enc_letters)
        self.__crossover_min_thresh = 1 #int(self.length / 3)
        self.__crossover_max_thresh = self.__length - 1 #2 * self.__crossover_min_thresh
        self.__enc_letters = enc_letters

    def swap_mutation(self, dec_map: Dict[str, str]) -> Tuple[str, List[Tuple[str, str]]]:
        keys = list(dec_map.keys())
        values = list(dec_map.values())

        # Choose 2 letters in random and swap their positions
        i, j = Selector.choose_n_random(self.__enc_letters, 2)
        c1, c2 = keys[i], keys[j]

        # Get permutation
        target_letters: List[str] = list(values[:])
        target_letters[i], target_letters[j] = values[j], values[i]
        
        return ''.join(target_letters), [(c1, c2)]

    def scramble_mutation(self, dec_map: Dict[str, str]) -> Tuple[str, List[Tuple[str, str]]]:
        keys = list(dec_map.keys())
        values = list(dec_map.values())

        i, j = Selector.choose_n_random(keys, 2)
        i, j = min(i, j), max(i, j)

        sub = values[i: j]
        shuffle(sub)
        new_values = deepcopy(values)
        new_values[i: j] = sub

        swaps = []
        for idx in range(i, j):
            swaps.append((values[idx], new_values[idx]))

        return ''.join(values), swaps

    def one_point_crossover(self, s1: str, s2: str) -> Tuple[str, str]:
        i = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)

        cross_1 = s1[:i]
        cross_1 += s2[i:]
        cross_2 = s2[:i]
        cross_2 += s1[i:]
        
        return cross_1, cross_2
    
    def __get_replace_key(self, arr1: str, arr2: str, res: List[str], start: int):
        k = arr1[start]
        t = arr2.index(k)
        k = arr1[t]

        while res[t]:
            t = arr2.index(k)
            k = arr1[t]
        
        return t
    
    def pmx_crossover(self, s1: str, s2: str) -> str:
        i = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)
        j = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)

        while i == j:
            j = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)

        crossover: List[str] = [''] * len(self.__enc_letters)
        for k in range(i, j + 1):
            crossover[k] = s1[k]

        for k in range(i, j + 1):
            if s2[k] not in crossover:
                index = self.__get_replace_key(s1, s2, crossover, k)
                crossover[index] = s2[k]
                
        for i, v in enumerate(crossover):
            if not v:
                crossover[i] = s2[i]
        
        return ''.join(crossover)
    
    def generate_pmx_crossover(self, samples: List[Sample], fitness_scores: List[float]) -> List[str]:
        # Choose 2 samples for crossover
        s1, s2 = Selector.choose_n_weighted_random(samples, fitness_scores, 2)
        co = self.pmx_crossover(''.join(s1.decode_letters), ''.join(s2.decode_letters))
        return [co]

    def order_crossover(self, s1: str, s2: str) -> Tuple[str, str]:
        i = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)

        cross1 = s1[:i]
        cross2 = s2[:i]

        for s in s2:
            if s not in cross1:
                cross1 += s

        for s in s1:
            if s not in cross2:
                cross2 += s

        return cross1, cross2

    def generate_order_crossover(self, samples: List[Sample], fitness_scores: List[float]) -> List[str]:
        # Choose 2 samples for crossover
        s1, s2 = Selector.choose_n_weighted_random(samples, fitness_scores, 2)
        co1, co2 = self.order_crossover(''.join(s1.decode_letters), ''.join(s2.decode_letters))

        while not is_valid(co1) or not is_valid(co2):
            s1, s2 = Selector.choose_n_weighted_random(samples, fitness_scores, 2)
            co1, co2 = self.order_crossover(''.join(s1.decode_letters), ''.join(s2.decode_letters))

        return [co1, co2]

    def generate_valid_crossover(self, samples: List[Sample], fitness_scores: List[float]) -> List[str]:
        # Choose 2 samples for crossover
        s1, s2 = Selector.choose_n_weighted_random(samples, fitness_scores, 2)
        co1, co2 = self.one_point_crossover(''.join(s1.decode_letters), ''.join(s2.decode_letters))

        while not is_valid(co1) or not is_valid(co2):
            s1, s2 = Selector.choose_n_weighted_random(samples, fitness_scores, 2)
            co1, co2 = self.one_point_crossover(''.join(s1.decode_letters), ''.join(s2.decode_letters))
        
        return [co1, co2]
