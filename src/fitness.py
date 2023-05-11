from typing import List, Dict, Callable, Tuple


def check_words_in_dict_ratio(dec: List[str], corpus: List[str]) -> float:
    """
    Check the ratio of decoded words that appear in the corpus
    :param dec: List of decoded words
    :param corpus: List of Corpus words
    :return: float: ratio
    """
    dec = set(dec)
    corpus = set(corpus)

    n_words_dec = len(dec)
    n_words_intersection = len(corpus & dec)

    return 100 * (n_words_intersection / n_words_dec)


def letters_freq_ratio(dec_letters_freq: Dict[str, float], corpus_letters_freq, measurement_func: Callable) -> float:
    freqs = [(dec_letters_freq[c], corpus_letters_freq[c]) for c in corpus_letters_freq.keys()]

    return measurement_func(freqs)


def MSE(freqs: List[Tuple[float, float]], rooted: bool = False) -> float:
    n_freqs = len(freqs)
    res = 0

    for dec_freq, corpus_freq in freqs:
        val = (dec_freq - corpus_freq) ** 2

        if rooted:
            val = val ** 0.5

        res += val

    return res / n_freqs
