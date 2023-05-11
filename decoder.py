from typing import List, Dict


class Decoder:
    @staticmethod
    def decode(enc: List[str], dec_map: Dict[str, str]) -> str:
        return ''.join([dec_map[c] for c in enc])

    @staticmethod
    def decode_words(enc_words: List[str], dec_map: Dict[str, str]) -> List[str]:
        decoded_words = []

        for word in enc_words:
            decoded_word = ''.join([dec_map[c] for c in word])
            decoded_words.append(decoded_word)

        return decoded_words