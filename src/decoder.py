from typing import List, Dict


class Decoder:
    @staticmethod
    def decode(enc: List[str], dec_map: Dict[str, str]) -> str:
        return ''.join([dec_map[c] for c in enc])
    
    @staticmethod
    def decode_words(enc: str, dec_map: Dict[int, int]) -> str:
        return enc.translate(dec_map)
