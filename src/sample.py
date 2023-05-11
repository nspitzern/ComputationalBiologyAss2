from typing import List
from random import shuffle


class Sample:
    def __init__(self, letters: List[str]):
        self.letters = letters
        self.shuffled_letters = list(letters[:])
        shuffle(self.shuffled_letters)
        self.create_decode_map()

    def create_decode_map(self):
        self.dec_map = {self.letters[i]: self.shuffled_letters[i] for i in range(len(self.letters))}

    def set_decode_letters(self, letters: List[str]):
        self.shuffled_letters = letters

    def switch_decode_letters(self, c1: str, c2: str):
        self.dec_map[c1], self.dec_map[c2] = self.dec_map[c2], self.dec_map[c1]

    def __eq__(self, other):
        return self.shuffled_letters == other.shuffled_letters