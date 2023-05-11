from typing import Dict, List
from random import shuffle


class Sample:
    def __init__(self, letters: List[str]):
        decode_letters = list(letters[:])
        shuffle(decode_letters)
        self.__dec_map: Dict[str, str] = {letters[i]: decode_letters[i] for i in range(len(letters))}
    
    @property
    def dec_map(self):
        return self.__dec_map

    @property
    def decode_letters(self) -> List[str]:
        return list(self.__dec_map.values())
    
    def swap(self, c1: str, c2: str):
        self.__dec_map[c1], self.__dec_map[c2] = self.__dec_map[c2], self.__dec_map[c1]