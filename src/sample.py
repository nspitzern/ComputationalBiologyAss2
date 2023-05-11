from typing import List
from random import shuffle


class Sample:
    def __init__(self, letters: List[str]):
        self.__decode_letters = list(letters[:])
        shuffle(self.__decode_letters)

    @property
    def decode_letters(self) -> List[str]:
        return self.__decode_letters

    def swap(self, i: int, j: int):
        self.__decode_letters[i], self.__decode_letters[j] = self.__decode_letters[j], self.__decode_letters[i]