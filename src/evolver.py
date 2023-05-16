from typing import Dict, List, Tuple
from random import randint
from src.memory import Memory
from src.selector import Selector


class Evolver:
    def __init__(self, enc_letters: List[str]):
        self.length = len(enc_letters)
        self.__crossover_min_thresh = 0 #int(self.length / 3)
        self.__crossover_max_thresh = self.length #2 * self.__crossover_min_thresh
        self.enc_letters = enc_letters

    def mutate(self, dec_map: Dict[str, str]) -> Tuple[str, str, str]:
        keys = list(dec_map.keys())
        values = list(dec_map.values())

        # Choose 2 letters in random and swap their positions
        i, j = Selector.choose_2_random(self.enc_letters)
        c1, c2 = keys[i], keys[j]

        # Get permutation
        target_letters: List[str] = list(values[:])
        target_letters[i], target_letters[j] = values[j], values[i]
        
        return ''.join(target_letters), c1, c2

    def crossover(self, s1: str, s2: str) -> Tuple[str, str]:
        i = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)

        cross_1 = s1[:i]
        cross_1 += s2[i:]
        cross_2 = s2[:i]
        cross_2 += s1[i:]
        
        return cross_1, cross_2

    def generate_valid_crossover(self, samples: List[str], memory: Memory) -> Tuple[str, str]:
        # Choose 2 samples for crossover
        i, j = Selector.choose_2_random(samples)
        co1, co2 = self.crossover(''.join(samples[i].decode_letters), ''.join(samples[j].decode_letters))

        while co1 in memory or co2 in memory:
            i, j = Selector.choose_2_random(samples)
            co1, co2 = self.crossover(''.join(samples[i].decode_letters), ''.join(samples[j].decode_letters))
        
        return co1, co2
