import numpy as np
from typing import List, Dict, Callable, Set, Tuple
from collections import Counter


def check_words_in_dict_ratio(dec: List[str], corpus: Set[str]) -> float:
    """
    Check the ratio of decoded words that appear in the corpus
    :param dec: List of decoded words
    :param corpus: List of Corpus words
    :return: float: ratio
    """
    n_words_dec = len(dec)

    count = 0
    for w in dec:
        if w in corpus:
            count += 1

    return count / n_words_dec


def word_correctness_by_len(dec: List[str], corpus: Set[str]) -> float:
    """
    Calculate the fitness by the correct words length compared to total length.

    :param dec: List of decoded words
    :param corpus: List of Corpus words
    :return: float: fitness
    """
    total_let_count = 0
    correct_let_count = 0
    
    for w in dec:
        length = len(w)
        total_let_count += length

        if w in corpus:
            correct_let_count += length

    return correct_let_count / total_let_count


def get_let_freq(dec: str):
    counter = Counter(dec)

    try:
        counter.pop(' ')
    finally:
        pass

    return { k: v / counter.total() for k, v in counter.items() }


def get_bigrams_freq(dec: str) -> Dict[str, float]:
    freqs = dict()
    length = len(dec)
    dec = dec.replace(' ', '')
    bigrams = list(zip(dec, dec[1:]))

    c = Counter(bigrams)
    for k, v in c.items():
        freqs[k[0] + k[1]] = v / length
    return dict(freqs)


def letters_freq_ratio(dec: str, corpus_letters_freq: Dict[str, float], measurement_func: Callable) -> float:
    dec_letters_freq = get_let_freq(dec)
    freq1 = [dec_letters_freq.get(c, 0) for c in corpus_letters_freq.keys()]
    freq2 = [corpus_letters_freq[c] for c in corpus_letters_freq.keys()]
    return measurement_func(freq1, freq2)


def MSE(freq1: List[float], freq2: List[float], rooted: bool = False) -> float:
    n_freqs = len(freq2)
    res = 0

    for dec_freq, corpus_freq in zip(freq1, freq2):
        val = (dec_freq - corpus_freq) ** 2
        res += val / n_freqs

    if rooted:
        res = res ** 0.5
    return res


def NMSE(freq1: List[float], freq2: List[float]) -> float:
    n_freqs = len(freq1)
    res = sum([(dec_freq - corpus_freq) ** 2 for dec_freq, corpus_freq in zip(freq1, freq2)])
    res /= np.var(freq2)

    return res / n_freqs


def abs_diff(freq1: List[float], freq2: List[float]) -> float:
    return sum([abs(f1 - f2) for f1, f2 in zip(freq1, freq2)])


def minus_freq_diff(freq1: List[float], freq2: List[float]) -> float:
    length = len(freq2)
    return sum([1 - abs(f1 - f2) for f1, f2 in zip(freq1, freq2)]) / length
