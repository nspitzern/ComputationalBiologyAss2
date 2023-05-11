import os
from typing import List, Dict, Tuple
from string import punctuation, whitespace


def parse_dict(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        d = [word.lower().strip() for word in f.readlines()]

    return d


def parse_letters_freq(file_path: str) -> Dict[str, float]:
    with open(file_path, 'r', encoding='utf-8') as f:
        d = {word.split('\t')[1].lower().strip(): float(word.split('\t')[0].strip())
             for word in f.readlines() if word not in whitespace and word != '\t#REF!\n'}

    return d

def parse_encoded(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return os.linesep.join(f.readlines()).lower()
