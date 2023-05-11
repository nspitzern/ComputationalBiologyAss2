from typing import Dict, List, Set
from src.files_parser import parse_dict, parse_encoded, parse_letters_freq
from src.generator import Generator, Sample
from src.memory import Memory
from src.selector import Selector
from src.decoder import Decoder
from src.fitness import check_words_in_dict_ratio


class Simulator:
    def __init__(self, num_samples: int, fitness_goal: int) -> None:
        self.enc_words, enc_letters = parse_encoded('enc.txt')
        self.dictionary: Set[str] = set(parse_dict('dict.txt'))
        freq_1_letter: Dict[str, float] = parse_letters_freq('Letter_Freq.txt')
        freq_2_letter: Dict[str, float] = parse_letters_freq('Letter2_Freq.txt')

        self.__letters = list(sorted(freq_1_letter.keys()))
        self.__memory: Memory = Memory()
        self.__fitness_goal: float = fitness_goal
        self.__generator: Generator = Generator(self.__letters)
        self.__selector: Selector = Selector()
        self.__samples: List[Sample] = self.__generator.generate_random(num_samples)

    def run(self):
        decs_words = [Decoder.decode_words(self.enc_words, s.dec_map) for s in self.__samples]
        fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in decs_words]
        
        while all(fitness_scores) < self.__fitness_goal:
            print(f'{max(fitness_scores)}%')

            elite_samples = self.__selector.select_elite(self.__samples, fitness_scores, self.__fitness_goal)

            for s in self.__samples:
                mutation, c1, c2 = self.__generator.generate_mutation(s.dec_map)
                while mutation in self.__memory.records:
                    mutation: str = self.__generator.generate_mutation(s.dec_map)
                self.__memory.add(mutation)
                s.swap(c1, c2)

            # Decode the encrypted file
            decs_words = [Decoder.decode_words(self.enc_words, s.dec_map) for s in self.__samples]
            # Calculate fitness score for each decode
            fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in decs_words]
