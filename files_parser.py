from typing import List, Dict
from string import punctuation, whitespace


def parse_dict(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        d = [word.strip() for word in f.readlines()]

    return d


def parse_letters_freq(file_path: str) -> Dict[str, float]:
    with open(file_path, 'r', encoding='utf-8') as f:
        d = {word.split('\t')[1].strip(): float(word.split('\t')[0].strip())
             for word in f.readlines() if word not in whitespace and word != '\t#REF!\n'}

    return d


def parse_encoded(file_path: str) -> List[str]:
    letters_enc = []
    words_enc = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line in whitespace:
                continue

            words = line.split(' ')

            for word in words:
                word = word.strip()
                words_enc.append(word)

                for l in word:
                    if l in punctuation:
                        continue
                    letters_enc.append(l)

    return letters_enc
