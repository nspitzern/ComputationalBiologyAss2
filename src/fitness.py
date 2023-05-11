from typing import List, Dict, Callable, Set, Tuple


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

    return 100 * count / n_words_dec


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
