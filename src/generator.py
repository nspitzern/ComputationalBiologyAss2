from typing import Dict, List, Tuple
from random import sample
from src.sample import Sample


class Generator:
    def __init__(self, enc_letters: List[str]):
        self.enc_letters = enc_letters

    def generate_random(self, n_samples: int) -> List[Sample]:
        g = []

        # Map each letter in the encrypted sentence to one decoding letter
        for _ in range(n_samples):
            s = Sample(self.enc_letters)
            g.append(s)

        return g

    def generate_mutation(self, dec_map: Dict[str, str]) -> Tuple[str, str, str]:
        keys = list(dec_map.keys())
        values = list(dec_map.values())

        # Choose 2 letters in random and swap their positions
        i, j = sample(range(len(self.enc_letters)), 2)
        c1, c2 = keys[i], keys[j]

        # Get permutation
        target_letters: List[str] = list(values[:])
        target_letters[i], target_letters[j] = values[j], values[i]
        
        return ''.join(target_letters), c1, c2

    def generate_crossover(self, s1: Sample, s2: Sample) -> Sample:
        raise NotImplementedError

