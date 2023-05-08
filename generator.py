from string import punctuation, ascii_lowercase
from typing import List
from random import choice


class Generator:
    def __init__(self, sentence_length: int):
        self.enc_length = sentence_length

    def generate_random(self, n_samples: int) -> List[str]:
        g = []

        for i in range(n_samples):
            g.append(''.join([choice(ascii_lowercase) for _ in range(self.enc_length)]))

        return g