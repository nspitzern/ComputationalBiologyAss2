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
        for i in range(n_samples):
            s = Sample(self.enc_letters)
            g.append(s)

        return g

    def generate_mutation(self, sample_sentence: Sample) -> Sample:
        decode_letters = sample_sentence.shuffled_letters

        # Choose 2 letters in random and swap their positions
        i, j = sample(range(len(decode_letters)), 2)
        decode_letters[i], decode_letters[j] = decode_letters[j], decode_letters[i]
        sample_sentence.set_decode_letters(decode_letters)

        # Update the decoding map accordingly
        c1, c2 = decode_letters[i], decode_letters[j]
        sample_sentence.switch_decode_letters(c1, c2)

        return sample_sentence

    def generate_crossover(self, s1: Sample, s2: Sample) -> Sample:
        raise NotImplementedError

