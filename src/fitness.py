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


def letters_freq_ratio(dec_letters_freq: Dict[str, float], corpus_letters_freq, measurement_func: Callable) -> float:
    freqs = [(dec_letters_freq[c], corpus_letters_freq[c]) for c in corpus_letters_freq.keys()]

    return measurement_func(freqs)


# def letters_freq_ratio(dec: str, corpus_letters_freq, measurement_func: Callable) -> float:
#     dec_letters_freq = get_let_freq(dec)
#     freqs = [(dec_letters_freq.get(c, 0), corpus_letters_freq[c]) for c in corpus_letters_freq.keys()]

#     return measurement_func(freqs)


def MSE(freqs: List[Tuple[float, float]], rooted: bool = False) -> float:
    n_freqs = len(freqs)
    res = 0

    for dec_freq, corpus_freq in freqs:
        val = (dec_freq - corpus_freq) ** 2

        if rooted:
            val = val ** 0.5

        res += val

    return res / n_freqs
