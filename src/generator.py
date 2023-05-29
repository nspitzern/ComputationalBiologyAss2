from typing import List
from src.sample import Sample


def generate_random(enc_letters: List[str], n_samples: int) -> List[Sample]:
    g = []

    # Map each letter in the encrypted sentence to one decoding letter
    for _ in range(n_samples):
        s = Sample(enc_letters)
        g.append(s)

    return g


def is_valid(letters: str) -> bool:
    return len(letters) == len(set(letters))
