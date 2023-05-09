from typing import List


def check_words_in_dict_ratio(dec: List[str], dictionary: List[str]) -> float:
    dec = set(dec)
    dictionary = set(dictionary)

    n_words_dec = len(dec)
    n_words_intersection = len(dictionary & dec)

    return 100 * (n_words_intersection / n_words_dec)
