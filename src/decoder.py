from typing import List, Dict


class Decoder:
    @staticmethod
    def decode(enc: List[str], dec_map: Dict[str, str]) -> str:
        return ''.join([dec_map[c] for c in enc])

    # @staticmethod
    # def decode_words(enc_words: List[str], dec_map: Dict[str, str]) -> List[str]:
    #     return [''.join([dec_map[c] for c in word]) for word in enc_words]
    
    # @staticmethod
    # def decode_words(enc_words: List[str], dec_map: Dict[str, str]) -> List[str]:
    #     return [''.join((map(lambda c: dec_map[c], w))) for w in enc_words]

    # @staticmethod
    # def decode_words(enc: str, dec_map: Dict[str, str]) -> str:
    #     return ''.join([dec_map.get(c, c) for c in enc])
    
    @staticmethod
    def decode_words(enc: str, dec_map: Dict[str, str]) -> str:
        return enc.translate(dec_map)

    # @staticmethod
    # def decode_words(enc: str, dec_map: Dict[str, str]) -> List[str]:
    #     return ''.join(map(lambda c: dec_map.get(c, c), enc))
