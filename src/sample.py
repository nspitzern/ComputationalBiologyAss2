from typing import Dict, List, Tuple
from random import shuffle


class Sample:
    def __init__(self, letters: List[str], decode_letters: str = None):
        if not decode_letters:
            decode_letters = list(letters[:])
            shuffle(decode_letters)
        self.__dec_map: Dict[str, str] = {letters[i]: decode_letters[i] for i in range(len(letters))}
        self.__dec_map_int: Dict[int, int] = {ord(letters[i]): ord(decode_letters[i]) for i in range(len(letters))}

    def __repr__(self):
        return ''.join(self.decode_letters)
    
    @property
    def dec_map(self):
        return self.__dec_map
    
    @property
    def dec_map_int(self):
        return self.__dec_map_int

    def get_dec_map_as_table(self, letters):
        s = ''
        for c in letters:
            s += f'{c} {self.__dec_map.get(c)}\n'

        return s

    @property
    def decode_letters(self) -> List[str]:
        return list(self.__dec_map.values())

    def swap(self, swaps: List[Tuple[str, str]]):
        for c1, c2 in swaps:
            self.__dec_map[c1], self.__dec_map[c2] = self.__dec_map[c2], self.__dec_map[c1]

            i, j = ord(c1), ord(c2)
            self.__dec_map_int[i], self.__dec_map_int[j] = self.__dec_map_int[j], self.__dec_map_int[i]