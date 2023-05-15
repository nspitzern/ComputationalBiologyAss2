from typing import Dict, List, Tuple
from random import sample, randint
from src.generator import is_valid
from src.sample import Sample


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
        i, j = sample(range(len(self.enc_letters)), 2)
        c1, c2 = keys[i], keys[j]

        # Get permutation
        target_letters: List[str] = list(values[:])
        target_letters[i], target_letters[j] = values[j], values[i]
        
        return ''.join(target_letters), c1, c2

    def crossover(self, s1: str, s2: str) -> Tuple[str, str]:
        i = randint(self.__crossover_min_thresh, self.__crossover_max_thresh)

        cross_1 = s1[:i]
        cross_1.extend(s2[i:])
        cross_2 = s2[:i]
        cross_2.extend(s1[i:])
        
        return cross_1, cross_2
    
    # def generate_valid_crossover(self, s1: str, s2: str) -> Tuple[str, str]:
    #     cross_1, cross_2 = self.generate_crossover(s1, s2)
    #     while not is_valid(cross_1) and not is_valid(cross_2):
    #         cross_1, cross_2 = self.generate_crossover(s1, s2)
        
    #     return cross_1, cross_2
