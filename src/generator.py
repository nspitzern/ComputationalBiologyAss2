from typing import List
from random import sample
from src.sample import Sample


class Generator:
    def __init__(self, enc_letters: List[str], sentence_length: int):
        self.enc_length = sentence_length
        self.enc_letters = enc_letters

    def generate_random(self, n_samples: int) -> List[Sample]:
        g = []

        # Map each letter in the encrypted sentence to one decoding letter
        for _ in range(n_samples):
            s = Sample(self.enc_letters)
            g.append(s)

        return g

    def generate_mutation(self, sentence_sample: Sample) -> Sample:
        decode_letters = sentence_sample.shuffled_letters

        # Choose 2 letters in random and swap their positions
        i, j = sample(range(len(decode_letters)), 2)
        sentence_sample.switch_letters(decode_letters[i], decode_letters[j])

    def generate_crossover(self, s1: Sample, s2: Sample) -> Sample:
        raise NotImplementedError

