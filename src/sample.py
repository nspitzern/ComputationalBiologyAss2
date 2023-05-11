from typing import Dict, List
from random import shuffle


class Sample:
    def __init__(self, letters: List[str]):
        shuffled_letters = list(letters[:])
        shuffle(shuffled_letters)

        self.dec_map: Dict[str, str] = self.create_decode_map(letters, shuffled_letters)

    @property
    def shuffled_letters(self) -> List[str]:
        return list(self.dec_map.values())

    def create_decode_map(self, letters: List[str], shuffled_letters: List[str]) -> Dict[str, str]:
        return {letters[i]: shuffled_letters[i] for i in range(len(letters))}

    def switch_letters(self, c1: str, c2: str):
        self.dec_map[c1], self.dec_map[c2] = self.dec_map[c2], self.dec_map[c1]